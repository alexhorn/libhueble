import signal
from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver
from hap_lamp import LampAccessory

LAMPS = {
    'Hue Go': '00:11:22:33:44:55:66'
}

def get_bridge(driver):
    bridge = Bridge(driver, 'Laemp Bridge')
    for name, address in LAMPS.items():
        lamp = LampAccessory(driver, display_name=name, address=address)
        bridge.add_accessory(lamp)
    return bridge

driver = AccessoryDriver(port=51826)
driver.add_accessory(accessory=get_bridge(driver))

signal.signal(signal.SIGTERM, driver.signal_handler)

driver.start()
