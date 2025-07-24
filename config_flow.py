from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .hitron_api import HitronClient


class HitronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            host = user_input["host"]
            username = user_input["username"]
            password = user_input["password"]

            client = HitronClient(host, username, password)
            try:
                # Replace with a real connection test
                status = await self.hass.async_add_executor_job(client.get_status)
                if status is None:
                    raise Exception("No status")
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Hitron ({host})",
                    data=user_input
                )

        data_schema = vol.Schema({
            vol.Required("host", default="192.168.0.1"): str,
            vol.Required("username", default="admin"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )