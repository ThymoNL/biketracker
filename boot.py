# boot.py -- run on boot-up
from network import LoRa
import pycom
import ubinascii
import socket
import time
import lora_keys as keys

# Disable LTE radio
if pycom.lte_modem_en_on_boot():
    print("LTE is enabled. Disabling...")
    pycom.lte_modem_en_on_boot(False)

# Join LoRa network
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print(ubinascii.hexlify(lora.mac()).upper().decode('utf-8'))

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(keys.dev_eui, keys.app_eui, keys.app_key), timeout=0)

# wait until network joined
while not lora.has_joined():
    time.sleep(2.5)
    print("Waiting to join...")

print("Joined LoRaWAN")