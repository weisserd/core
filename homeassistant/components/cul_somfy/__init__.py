"""The CUL Somfy RTS integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# CUL stick is a remote, covers are allowed
PLATFORMS: list[Platform] = [Platform.REMOTE, Platform.COVER]

# LATER Only allow one stick - https://github.com/weisserd/core/blob/cul_somfy/homeassistant/components/enocean/__init__.py#L18


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CUL Somfy RTS from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, Platform.REMOTE)
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
