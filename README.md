# lämp

A bridge that allows you to control your Bluetooth-capable Philips Hue lights via HomeKit.

## Setup

### Pair your lamp

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


### Add the bridge to the Home app

1. Run from a terminal:
   ```
   sudo ./venv/bin/python3 hap_bridge.py
   ```
2. Open the *Home* app and tap *Add device*
3. Scan the QR code displayed in the terminal


## Compatibility

Works on Raspbian Buster.

Sometimes it also works on Windows 10 20H2, but it is very flaky.
