from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator, UpdateFailed
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT, DEVICE_CLASS_SIGNAL_STRENGTH

from .const import DOMAIN
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]

    async def async_update_data():
        try:
            return await hass.async_add_executor_job(client.get_status)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Hitron modem: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="hitron modem",
        update_method=async_update_data,
        update_interval=60,  # seconds
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        HitronSensor(coordinator, "Uptime", "uptime", "mdi:clock-outline"),
        HitronSensor(coordinator, "Signal Strength", "signal_strength", "mdi:wifi"),
        HitronSensor(coordinator, "Connected", "connected", "mdi:lan-connect"),
    ]

    async_add_entities(sensors)


class HitronSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, key, icon):
        super().__init__(coordinator)
        self._attr_name = f"Hitron {name}"
        self._key = key
        self._attr_icon = icon
        self._attr_unique_id = f"hitron_{key}"

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)