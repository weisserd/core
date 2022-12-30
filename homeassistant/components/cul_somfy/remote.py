"""Representation of a CUL stick."""

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_SW_VERSION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CUL stick remote entity based on a config entry."""
    entities = []
    entities.append(CULStick(config_entry.data["device"]))

    async_add_entities(entities)


class CULStick(RemoteEntity):
    """Representation of a CUL stick."""

    _device = ""
    _attr_is_on = True
    _attr_available = True
    _should_poll = False

    def __init__(self, device: str) -> None:
        """Initialize the remote."""
        self._device = device
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_name = "CUL Stick " + device
        # LATER config states for codes

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._device

    @property
    def device_info(self) -> DeviceInfo:
        """Device information."""
        info = DeviceInfo(
            # LATER Get information from USB Port
            identifiers={(DOMAIN, self._device)},
            manufacturer="busware.de",
            name="CUL Stick",
            model="Model CUL433",
        )

        info[ATTR_SW_VERSION] = "xxxx"  # self._device.fw_version
        return info
