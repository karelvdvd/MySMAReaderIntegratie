from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower

from .const import CONF_HOST, CONF_PORT
from .sma import read_current_power


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors."""

    async_add_entities(
        [
            MySMAPowerSensor(hass, entry),
        ],
        True,
    )


class MySMAPowerSensor(SensorEntity):
    """SMA current power sensor."""

    _attr_name = "My SMA Current Power"
    _attr_unique_id = "mysma_current_power"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(self, hass, entry):
        self.hass = hass
        self.host = entry.data[CONF_HOST]
        self.port = entry.data[CONF_PORT]
        self._attr_native_value = None

    async def async_update(self):
        """Update sensor value."""

        self._attr_native_value = await read_current_power(
            self.hass,
            self.host,
            self.port,
        )