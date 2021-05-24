from bleak import BleakClient
from rgbxy import Converter, GamutC
from struct import pack, unpack

CHAR_POWER          = "932c32bd-0002-47a2-835a-a8d455b859dd"
CHAR_BRIGHTNESS     = "932c32bd-0003-47a2-835a-a8d455b859dd"
CHAR_COLOR          = "932c32bd-0005-47a2-835a-a8d455b859dd"

# Hue Go uses GamutC
# you might need GamutA or GamutB if you have a different model
converter = Converter(GamutC)

class Lamp(object):
    def __init__(self, address):
        self.client = BleakClient(address)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def get_power(self):
        return await self.client.read_gatt_char(CHAR_POWER)[0]

    async def set_power(self, on):
        await self.client.write_gatt_char(CHAR_POWER, bytes([1 if on else 0]), response=True)

    async def get_brightness(self):
        return await self.client.read_gatt_char(CHAR_BRIGHTNESS)[0] / 255

    async def set_brightness(self, brightness):
        await self.client.write_gatt_char(CHAR_BRIGHTNESS, bytes([max(min(int(brightness * 255), 254), 1)]), response=True)

    async def get_color_xy(self):
        buf = await self.client.read_gatt_char(CHAR_COLOR)
        x, y = unpack('<HH', buf)
        return x / 0xFFFF, y / 0xFFFF

    async def set_color_xy(self, x, y):
        # Hue expects CIE XY coordinates converted to two 16-bit little-endian integers
        buf = pack('<HH', int(x * 0xFFFF), int(y * 0xFFFF))
        await self.client.write_gatt_char(CHAR_COLOR, buf, response=True)

    async def get_color_rgb(self):
        x, y = await self.get_color_xy()
        return converter.xy_to_rgb(x, y)

    async def set_color_rgb(self, r, g, b):
        x, y = converter.rgb_to_xy(r, g, b)
        await self.set_color_xy(x, y)
