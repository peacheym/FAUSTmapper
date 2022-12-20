from re import L
import libmapper as mpr


dev = mpr.Device("prod")
sensor1 = dev.add_signal(mpr.Direction.OUTGOING, "sensor1", 1, mpr.Type.FLOAT,
                         "V", 0.0, 5.0)

value = 0.5

while(1):
    value *= -1 
    print(value)
    sensor1.set_value(float(value))
    dev.poll(50)