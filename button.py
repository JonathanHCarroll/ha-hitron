from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([HitronRebootButton(client)])

class HitronRebootButton(ButtonEntity):
    def __init__(self, client):
        self._attr_name = "Reboot Hitron Modem"
        self.client = client

    async def async_press(self):
        await self.hass.async_add_executor_job(self.client.reboot)