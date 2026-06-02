from homeassistant.components.sensor import SensorEntity


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors."""

    async_add_entities(
        [
            MySMATestSensor(),
        ]
    )


class MySMATestSensor(SensorEntity):
    """Test sensor."""

    _attr_name = "My SMA Test"
    _attr_native_value = "OK"
    _attr_unique_id = "mysma_test_sensor"