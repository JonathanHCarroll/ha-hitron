from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from .const import DOMAIN
from .hitron_api import HitronClient

PLATFORMS = ["sensor", "button"]

async def async_setup(hass: HomeAssistant, config: dict):
    return True



async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    data = {**entry.data, **entry.options}
    client = HitronClient(
        host=data.get("host", "192.168.0.1"),
        username=data.get("username", "cusadmin"),
        password=data.get("password", "admin")
    )

    # 1. Log in first
    login_result = await hass.async_add_executor_job(client.post_login)
    if not login_result or login_result.get("result") != "success":
        raise ConfigEntryNotReady(f"Unable to log in to Hitron modem: {login_result}")

    # 2. Now fetch sysinfo
    result = await hass.async_add_executor_job(client.get_sysinfo)
    if not result:
        raise ConfigEntryNotReady("Unable to connect to Hitron modem after login")

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
  await async_unload_entry(hass, entry)
  await async_setup_entry(hass, entry)