"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=6448,
    help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    # Begin Recordings
    client.send_message("/wekinator/control/startRecording", "")
    
    
    print("Sending Five 1s")
    for x in range(50):
        client.send_message("/wek/inputs", 1)
        
    print("waiting...")
    test = input()

    print("Sending Five -1s")
    for x in range(50):
        client.send_message("/wek/inputs", -1)
    
    client.send_message("/wekinator/control/stopRecording", "")
    
    curr = 1
    while True:
        print(curr)
        client.send_message("/wek/inputs", curr)
        curr *= -1
        time.sleep(5)