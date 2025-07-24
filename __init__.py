from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .hitron_api import HitronClient

PLATFORMS = ["sensor", "button"]

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    client = HitronClient()  # Add credentials or host if needed
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
  data = {**entry.data, **entry.options}
  client = HitronClient(
      host=data["host"],
      username=data["username"],
      password=data["password"]
  )
  hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client
  await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
  return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
  await async_unload_entry(hass, entry)
  await async_setup_entry(hass, entry)