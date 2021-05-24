# lämp 🦋

A bridge for controlling your Bluetooth-capable Philips Hue lights via HomeKit.

It uses HAP-python to provide a bridge that can be added to the iOS Home app.
The lights are controlled directly using Bluetooth Low Energy (BLE), without the need for additional hardware.
You can also use the included lamp.py to implement your own project in Python.

## Setup

### Install

```
sudo apt install python3 python3-venv python3-wheel avahi-utils
git clone https://github.com/alexhorn/laemp.git
cd laemp
python3 -m venv venv
./venv/bin/pip3 install -r requirements.txt
```

### Pair your lights

1. Use the Hue BT app to factory-reset your light. Otherwise it will refuse to bond to your computer.
2. Open the bluetoothctl shell:
   ```
   sudo bluetoothctl
   ```
3. Start the discovery:
   ```
   scan on
   ```
4. Write down the MAC address of your light.
5. Pair to your light:
   ```
   pair [MAC address]
   trust [MAC address]
   ```
6. Done, you can now pair the light to your phone again.

### Create config

1. Create a `config.ini` using `config.ini.example` as a reference.
2. Add the names and MAC addresses of your paired lights.

### Add the bridge to the Home app

1. Run from a terminal (you need to use either *sudo* or *setcap* to access Bluetooth):
   ```
   sudo ./venv/bin/python3 hap_bridge.py
   ```
2. Open the *Home* app and tap *Add device*.
3. Scan the QR code displayed in the terminal.


## Compatibility

Works on Raspbian Buster.

Sometimes it also works on Windows 10 20H2, but it is very flaky.

## Credits

This is pieced together from the reverse engineering efforts of other people on the internet.

Sources:
* https://github.com/npaun/philble
* https://gist.github.com/shinyquagsire23/f7907fdf6b470200702e75a30135caf3
* https://www.reddit.com/r/Hue/comments/eq0y3y/philips_hue_bluetooth_developer_documentation/
