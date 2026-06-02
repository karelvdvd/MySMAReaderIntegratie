from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .sma import test_connection
from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)


class MySMAReaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My SMA Reader."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(
                    CONF_PORT,
                    default=DEFAULT_PORT,
                ): int,
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=DEFAULT_SCAN_INTERVAL,
                ): int,
            }
        )

        if user_input is not None:

            can_connect = await test_connection(
                self.hass,
                user_input[CONF_HOST],
                user_input[CONF_PORT],
            )

            if can_connect:
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

            return self.async_show_form(
                step_id="user",
                data_schema=schema,
                errors={"base": "cannot_connect"},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )