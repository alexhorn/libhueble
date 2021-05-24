from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB
from lamp import Lamp
from colorsys import rgb_to_hsv, hsv_to_rgb
import asyncio

class LampAccessory(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, *args, address, **kwargs):
        super().__init__(*args, **kwargs)
        self.lamp = Lamp(address)

        serv_light = self.add_preload_service('Lightbulb', chars=['On', 'Hue', 'Saturation', 'Brightness'])
        self.char_on = serv_light.configure_char('On', setter_callback=self._async_callback(self.set_on))
        self.char_hue = serv_light.configure_char('Hue', setter_callback=self._async_callback(self.set_hue))
        self.char_saturation = serv_light.configure_char('Saturation', setter_callback=self._async_callback(self.set_saturation))
        self.char_brightness = serv_light.configure_char('Brightness', setter_callback=self._async_callback(self.set_brightness))

    def _async_callback(self, coro):
        return lambda val: asyncio.create_task(coro(val))

    async def run(self):
        self.loop = asyncio.get_event_loop()
        self.lock = asyncio.Lock(loop=self.loop)
        await self.lamp.connect()

    async def stop(self):
        await self.lamp.disconnect()

    async def set_on(self, value):
        async with self.lock:
            await self.lamp.set_power(value)

    async def set_hue(self, hue):
        async with self.lock:
            _, s, b = rgb_to_hsv(*await self.lamp.get_color_rgb())
            await self.lamp.set_color_rgb(*hsv_to_rgb(hue / 360, s, b))

    async def set_saturation(self, saturation):
        async with self.lock:
            h, _, b = rgb_to_hsv(*await self.lamp.get_color_rgb())
            await self.lamp.set_color_rgb(*hsv_to_rgb(h, saturation / 100, b))

    async def set_brightness(self, brightness):
        async with self.lock:
            await self.lamp.set_brightness(brightness / 100)
