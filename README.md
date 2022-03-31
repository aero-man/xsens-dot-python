# Xsens DOT Python Server

Connect to Xsens DOT wearable sensors via Python.

### Requirements
* [Bluepy](https://github.com/IanHarvey/bluepy)
* [Numpy](https://numpy.org/)
* One or more [Xsens DOT sensors](https://www.xsens.com/xsens-dot)

### Installation

Enter this in your command prompt or terminal to install necessary Python modules via Pip:  
`pip install -r requirements.txt`

### How to Run
There are generally two steps to connecting to any Bluetooth device: Scanning for all Bluetooth devices near you, and pairing/connecting to the device.
1. Find the DOTs with `$ python blescan.py`. `blescan.py` finds all Bluetooth devices in your area, including phones, laptops, and lightbulbs, and will print them all to the console/command line/Terminal.
2. Add the addresses of only the Xsens DOTs that were found to `device_addresses.csv`. The address will look like `aa:bb:cc:12:34:56`.
3. Connect to and start getting data from the DOTs by running `$ python server.py`. DOT data will be printed to the console.

### Known Bugs
There is a known issue where DOTs may send out messages that only have half the data elements they're supposed to. For example, if you turn on a mode that is supposed to give you accelerometer data and gyroscope data, you might only get accelerometer data. This may be an issue with the code in this repository or with the original Xsens code.

There is an [issue open here with Xsens themselves](https://github.com/xsens/xsens_dot_server/issues/11), but they're a Node shop rather than a Python shop, so the issue was not looked into further.

