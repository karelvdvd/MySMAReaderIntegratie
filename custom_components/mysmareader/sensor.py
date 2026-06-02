from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfTemperature
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up SMA sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            MySMASensor(
                coordinator,
                entry,
                key="current_power",
                name="Current Power",
                unit=UnitOfPower.WATT,
                device_class=SensorDeviceClass.POWER,
                state_class=SensorStateClass.MEASUREMENT,
            ),
            MySMASensor(
                coordinator,
                entry,
                key="energy_today",
                name="Energy Today",
                unit=UnitOfEnergy.KILO_WATT_HOUR,
                device_class=SensorDeviceClass.ENERGY,
                state_class=SensorStateClass.TOTAL_INCREASING,
                scale=0.001,
            ),
            MySMASensor(
                coordinator,
                entry,
                key="temperature",
                name="Temperature",
                unit=UnitOfTemperature.CELSIUS,
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                scale=0.1,
            ),
        ]
    )


class MySMASensor(CoordinatorEntity, SensorEntity):
    """SMA sensor."""

    def __init__(
        self,
        coordinator,
        entry,
        key,
        name,
        unit,
        device_class,
        state_class,
        scale=1,
    ):
        super().__init__(coordinator)

        self.key = key
        self.scale = scale
        self.entry = entry

        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "SMA Omvormer",
            "manufacturer": "SMA",
            "model": "SMA Sunny Tripower 7000 ",
        }

    @property
    def native_value(self):
        """Return sensor value."""
        value = self.coordinator.data.get(self.key)

        if value is None:
            return None

        return round(value * self.scale, 2)