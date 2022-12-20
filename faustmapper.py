import argparse
import threading
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import requests
import libmapper as mpr


def print_compute_handler(unused_addr, *args):
    try:
        for i, param_name in enumerate(signals.keys()):
            value = (
                (args[i+1] * (float(signals[param_name]['max']) - float(signals[param_name]['min'])))) + float(signals[param_name]['min'])  # Use appropriate range.
            send_update(param_name, value)
    except ValueError:
        pass


def start_server(ip, port):
    print("Starting OSC Server")
    server = osc_server.ThreadingOSCUDPServer(
        (ip, port), dispatcher)
    print("Serving on {}\n".format(server.server_address))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()


def start_client(ip, port):
    print("Starting OSC Client\n")
    client = udp_client.SimpleUDPClient(ip, port)  # client variable is unused
    thread = threading.Thread()
    thread.start()


def send_update(param_name, value):

    http_string = "http://localhost:5510{}?value={}".format(
        signals[param_name]['address'], value)

    # print(http_string) # If DEBUGGING
    requests.get(http_string)


def sig_h(sig, event, id, val, time):
    '''
    Define a signal handler.
    '''
    try:
        # print(val)
        send_update(sig['name'], val)
    except Exception as e:
        print('exception', e)
        print(sig, val)


def parse_synth_params(input):
    # Todo: TEST this recursive function to ensure it truly works with all FAUST synths

    param_objs = []

    for i in input:
        if i.get('items'):
            param_objs.extend(parse_synth_params(i['items']))
        else:
            param_objs.append(i)
    return param_objs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=12000, help="The port to listen on")
    parser.add_argument("--mapping-target", default="libmapper",
                        help="The mapping platform you wish to use. Ie: \"libmapper\" or \"wekinator\".")
    parser.add_argument("--debug", type=bool, default=False,
                        help="Flag to print additional information when debugging.")
    parser.add_argument("--save-state", type=bool, default=False,
                        help="Flag to save the state to a predetermined database.")
    args = parser.parse_args()

    try:
        # Fetch name of FAUST program
        full_json = requests.get("http://localhost:5510/JSON")
        synth_name = full_json.json()['name']
        top_ui = full_json.json()['ui'][0]['label']
        all_params = requests.get("http://localhost:5510/{}".format(top_ui))

    except Exception as e:
        if args.debug:
            print(e)
        print("Error: No FAUST synth running over HTTP.")
        print("Shutting down ...")
        exit()

    signals = {}

    # --- LIBMAPPER ---
    if args.mapping_target == "libmapper":
        # Init libmapper device

        graph = mpr.Graph()
        graph.set_interface("wlp0s20f3")
        print("Using interface:", graph.get_interface())
        dev = mpr.Device(synth_name, graph)
        # Do some error checking on this.
        for param in parse_synth_params(full_json.json()['ui'][0]['items']):

            # Dynamically add libmapper signals based on each parameter.
            if param.get('min'):
                s = dev.add_signal(mpr.Direction.INCOMING, param['label'], 1, mpr.Type.FLOAT, None, float(
                    param['min']), float(param['max']), None, sig_h)
                signals[param['label']] = {
                    'sig': s, 'min': param['min'], 'max': param['max'], 'address': param['address']}
            # If there is no min/max values for this faust parameter.
            else:
                s = dev.add_signal(
                    mpr.Direction.INCOMING, param['label'], 1, mpr.Type.FLOAT, None, None, None, None, sig_h)
                signals[param['label']] = {
                    'sig': s, 'address': param['address']}

        print("Libmapper Signals ->", signals.keys())
        print("...running libmapper")

        while True:
            dev.poll()

    # --- WEKINATOR ---
    elif args.mapping_target == "wekinator":
        dispatcher = dispatcher.Dispatcher()
        dispatcher.map("/wek/outputs", print_compute_handler, "Wekinator")
        for param in parse_synth_params(full_json.json()['ui'][0]['items']):
            if param.get('min'):
                signals[param['label']] = {
                    'min': param['min'], 'max': param['max'], 'address': param['address']}

        print("Number of Wekinator Parameters:", len(signals), "\n")

        start_server(args.ip, args.port)
        start_client('localhost', 6448)

        print("...running wekinator")
