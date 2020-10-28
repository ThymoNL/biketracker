# main.py
from network import LoRa
from pytrack import Pytrack
from L76GNSS import L76GNSS
import machine
import pycom
import socket
import gc
import time
import struct
import ubinascii


# Functions
def sendLoc():
    pos = gps.coordinates()
    lat = pos[0]
    lon = pos[1]

    if (lat is None or lon is None):
        pos_valid = 0
        lat = 0
        lon = 0
    else:
        pos_valid = 1

    #lora_data = bytearray(struct.pack("f", lat, lon), pos_valid)
    lora_data = "{0},{1},{2}".format(lat, lon, pos_valid)
    print(lora_data)

    pycom.heartbeat(False)
    pycom.rgbled(0x007f00)
    s.setblocking(True)
    s.send(lora_data)
    pycom.rgbled(0x0)
    s.setblocking(False)
    pycom.heartbeat(True)

# Main
gc.enable()
py = Pytrack()
gps = L76GNSS(py, timeout=30)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
pycom.heartbeat(True)

while True:
    sendLoc()
    time.sleep(10)
