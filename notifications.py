'''
This class allows a Python script to listen for data from an Xsens DOT.

You can attach this "delegate" to an Xsens DOT with `Peripheral.setDelegate()`.
NOTE: We give the Delegate class the address so it can print which device
      the data came from.
For example:
    my_periph = Peripheral("ab:cd:ef:12:34:56")
    delegate = XsensNotificationDelegate(my_periph.addr)
    my_periph.setDelegate(
'''

from bluepy import btle
import numpy as np

class XsensNotificationDelegate(btle.DefaultDelegate):
    def __init__(self, bluetooth_device_address):
        btle.DefaultDelegate.__init__(self)
        self.bluetooth_device_address = bluetooth_device_address
        print("XsensNotificationDelegate has been initialized")

    # Do something when sensor data is received. In this case, print it out.
    def handleNotification(self, cHandle, data):
        data_segments = np.dtype([('timestamp', np.uint32), ('quat_w', np.float32), ('quat_x', np.float32),
                       ('quat_y', np.float32), ('quat_z', np.float32)])
        human_readable_data = np.frombuffer(data, dtype=data_segments)
        formatted_data = str([x for x in human_readable_data.tolist()[0]][:-1])[1:-1]
        formatted_data = self.bluetooth_device_address + ", " + formatted_data
        print(formatted_data)

