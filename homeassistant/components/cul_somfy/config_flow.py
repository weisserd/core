"""Config flow for CUL Somfy RTS integration."""
from __future__ import annotations

import logging
from typing import Any

from serial import SerialException
import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import usb
from homeassistant.const import CONF_DEVICE
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)

# LATER Add automated USB detection


def _generate_unique_id(port: ListPortInfo) -> str:
    """Generate unique id from usb attributes."""
    return f"{port.vid}:{port.pid}_{port.serial_number}_{port.manufacturer}_{port.description}"


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CUL Somfy RTS."""

    VERSION = 1

    def __init__(self):
        """Initialise the config flow."""
        self.config = None
        self._com_ports_list = None
        self._default_com_port = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialised by the user."""

        errors: dict[str, str] | None = {}

        # Find devices
        ports = await self.hass.async_add_executor_job(serial.tools.list_ports.comports)
        _LOGGER.info("Ports: %s", ports)
        existing_devices = [
            entry.data[CONF_DEVICE] for entry in self._async_current_entries()
        ]
        unused_ports = [
            usb.human_readable_device_name(
                port.device,
                port.serial_number,
                port.manufacturer,
                port.description,
                port.vid,
                port.pid,
            )
            for port in ports
            if port.device not in existing_devices
        ]
        if not unused_ports:
            return self.async_abort(reason="no_devices_found")

        if user_input is not None:
            port = ports[unused_ports.index(str(user_input.get(CONF_DEVICE)))]
            dev_path = await self.hass.async_add_executor_job(
                usb.get_serial_by_id, port.device
            )
            errors = await self.validate_device_errors(
                dev_path=dev_path, unique_id=_generate_unique_id(port)
            )
            if errors is None:
                return self.async_create_entry(
                    title=DEFAULT_NAME + " - " + dev_path,
                    data={CONF_DEVICE: dev_path},
                )
        user_input = user_input or {}

        schema = vol.Schema({vol.Required(CONF_DEVICE): vol.In(unused_ports)})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def validate_device_errors(
        self, dev_path: str, unique_id: str
    ) -> dict[str, str] | None:
        """Handle common flow input validation."""
        self._async_abort_entries_match({CONF_DEVICE: dev_path})
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(updates={CONF_DEVICE: dev_path})
        try:
            # api = CulStick()
            # await api.test(dev_path)
            # LATER Check for information
            _LOGGER.info("Test CUL stick")
        except SerialException:
            return {"base": "cannot_connect"}
        else:
            return None
