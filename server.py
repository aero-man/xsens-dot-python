'''
Server that connects to and grabs data from Xsens DOT wearable IMUs.

Steps involved:
    - Connect to devices via their Bluetooth addresses. Add these to `device_addresses.csv`
    - Enable the CCCD for each device
    - Enable the Control Characteristic on each device
    - Set a notification delegate for each device to get actual sensor data
    - Start a loop to listen for sensor data

NOTES:
    - Handling of sensor data is determined in `XsensNotificationDelegate.handleNotification()`
    - CCCD = Client Characteristic Configuration Descriptor
'''


from bluepy import btle
import csv

from notifications import XsensNotificationDelegate

'''Handles and enable messages for Xsens DOTs' Bluetooth characteristics'''
CONTROL_CHARACTERISTIC = 32
SHORT_PAYLOAD_CHARACTERISTIC = 43
SHORT_PAYLOAD_CCCD = 44
MEDIUM_PAYLOAD_CHARACTERISTIC = 39
MEDIUM_PAYLOAD_CCCD = 40
CCCD_ENABLE_MESSAGE = b"\x01\x00"
ENABLE_MESSAGE = b"\x01\x01\x06"

'''Connect to Xsens DOTs via their Bluetooth addresses listed in `device_addresses.csv`.
You should use a command line tool to scan for these addresses or use Bluepy's `blescan.py`.
Scanning using this server is not yet supported.'''
ble_address_file = csv.reader(open("device_addresses.csv"))
bluetooth_addresses = [x[0] for x in ble_address_file]

peripherals = []
for addr in bluetooth_addresses:
    try:
        periph = btle.Peripheral(addr)
        peripherals.append(periph)
    except btle.BTLEDisconnectError:
        print("ERROR: Unable to connect to device at address {}".format(periph.addr))
print("Connected_peripherals: {}".format(peripherals))

'''Enable the CCCD for each device. This is necessary in addition to enabling the
measurement characteristic. The CCCD handles for medium payloads and short payloads are
different.'''
for periph in peripherals:
    periph.writeCharacteristic(SHORT_PAYLOAD_CCCD, CCCD_ENABLE_MESSAGE, withResponse=True)
    print("CCCD enabled for device: {}".format(periph.addr))

'''Enable the Control Characteristic on each device. This is the same whether we are
doing a short or medium payload measurement'''
print("ENABLE_MESSAGE: {}".format(ENABLE_MESSAGE))
for periph in peripherals:
    periph.writeCharacteristic(CONTROL_CHARACTERISTIC, ENABLE_MESSAGE, withResponse=True)
    print("Measurement enabled for device: {}".format(periph.addr))
    print(periph.readCharacteristic(CONTROL_CHARACTERISTIC))

for periph in peripherals:
    delegate = XsensNotificationDelegate(periph.addr)
    periph.setDelegate(delegate)

i = 1
while True:
    for periph in peripherals:
        if periph.waitForNotifications(1.0):
            pass
        else:
            print("No notification/data from sensor {} was received".format(periph.addr))
    i += 1

