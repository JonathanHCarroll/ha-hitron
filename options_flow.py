from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN


class HitronOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.data
        options_schema = vol.Schema({
            vol.Required("host", default=current.get("host", "192.168.0.1")): str,
            vol.Required("username", default=current.get("username", "admin")): str,
            vol.Required("password", default=current.get("password", "")): str,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors
        )


@callback
def async_get_options_flow(config_entry: config_entries.ConfigEntry):
    return HitronOptionsFlowHandler(config_entry)