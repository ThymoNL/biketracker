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
lora.set_battery_level(255) # We are on battery but have no way to measure this.

# Try to read state from nvram otherwise join a network using OTAA
lora.nvram_restore()
if not lora.has_joined():
    lora.join(activation=LoRa.OTAA, auth=(ubinascii.unhexlify(keys.dev_eui), ubinascii.unhexlify(keys.app_eui), ubinascii.unhexlify(keys.app_key)), timeout=0)

    # wait until network joined
    while not lora.has_joined():
        time.sleep(2.5)
        print("Waiting to join...")

    lora.nvram_save()

print("Joined LoRaWAN")
