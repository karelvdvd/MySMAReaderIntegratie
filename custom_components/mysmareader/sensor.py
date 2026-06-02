from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfTemperature

from .const import CONF_HOST, CONF_PORT
from .sma import read_sma_data


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up SMA sensors."""

    async_add_entities(
        [
            MySMASensor(
                hass,
                entry,
                key="current_power",
                name="My SMA Current Power",
                unit=UnitOfPower.WATT,
                device_class=SensorDeviceClass.POWER,
                state_class=SensorStateClass.MEASUREMENT,
            ),
            MySMASensor(
                hass,
                entry,
                key="energy_today",
                name="My SMA Energy Today",
                unit=UnitOfEnergy.KILO_WATT_HOUR,
                device_class=SensorDeviceClass.ENERGY,
                state_class=SensorStateClass.TOTAL_INCREASING,
                scale=0.001,
            ),
            MySMASensor(
                hass,
                entry,
                key="temperature",
                name="My SMA Temperature",
                unit=UnitOfTemperature.CELSIUS,
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                scale=0.01,
            ),
        ],
        True,
    )


class MySMASensor(SensorEntity):
    """SMA sensor."""

    def __init__(
        self,
        hass,
        entry,
        key,
        name,
        unit,
        device_class,
        state_class,
        scale=1,
    ):
        self.hass = hass
        self.host = entry.data[CONF_HOST]
        self.port = entry.data[CONF_PORT]
        self.key = key
        self.scale = scale

        self._attr_name = name
        self._attr_unique_id = f"mysma_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_native_value = None

    async def async_update(self):
        """Update sensor."""

        data = await read_sma_data(
            self.hass,
            self.host,
            self.port,
        )

        value = data.get(self.key)

        if value is None:
            self._attr_native_value = None
            return

        self._attr_native_value = round(value * self.scale, 2)