""" Helper function that uses arduinoserial to read samples from Arduino"""

import time
import os.path
import numpy as np


def read_from_arduino(duration=5,port=None,baud_rate=115200):
    import arduinoserial
    if port==None:
        raise ValueError("""You must specify a port! For example: \n data =
            read_from_arduino(duration=10,port=\"/dev/tty.usbserial-ABCDEFG\")
            """)

    arduino = arduinoserial.SerialPort(port, 115200)
    start = time.time()
    signal = []
    while time.time()-start < duration:
        try:
            signal.append(float(arduino.read_until('\n')))
        except:
            pass
    signal = np.asarray(signal,float)
    return signal

def read_from_file(filename='data.txt'):
    if not os.path.isfile(filename):
        raise ValueError("""You must specify correct filename! For example \n
            data = read_from_file(filename=\"data.txt\")""")
    signal = [line.rstrip('\n') for line in open(filename)]
    signal = np.asarray(signal,float)
    return signal