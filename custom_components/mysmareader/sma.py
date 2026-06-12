import socket
import logging

from pymodbus.client import ModbusTcpClient

_LOGGER = logging.getLogger(__name__)

SMA_UNIT_ID = 3
SMA_INVALID_U32 = 0x80000000


async def test_connection(hass, host, port, timeout=5):
    """Test TCP connection to SMA inverter."""

    def _test():
        try:
            _LOGGER.debug("Testing TCP connection to SMA inverter %s:%s", host, port)

            with socket.create_connection((host, port), timeout=timeout):
                _LOGGER.debug("TCP connection to SMA inverter succeeded")
                return True

        except OSError as err:
            _LOGGER.warning(
                "TCP connection to SMA inverter %s:%s failed: %r",
                host,
                port,
                err,
            )
            return False

    return await hass.async_add_executor_job(_test)


def _read_s32(client, address, name):
    """Read signed 32-bit value from SMA inverter."""

    _LOGGER.debug("Reading SMA register %s (%s)", address, name)

    result = client.read_holding_registers(
        address=address,
        count=2,
        device_id=SMA_UNIT_ID,
    )

    if result.isError():
        _LOGGER.warning("Error reading SMA register %s (%s): %s", address, name, result)
        return None

    if len(result.registers) < 2:
        _LOGGER.warning(
            "Invalid response length for SMA register %s (%s): %s",
            address,
            name,
            result.registers,
        )
        return None

    raw_value = (result.registers[0] << 16) + result.registers[1]

    if raw_value == SMA_INVALID_U32:
        _LOGGER.debug("SMA register %s (%s) returned invalid value", address, name)
        return None

    if raw_value >= 0x80000000:
        raw_value -= 0x100000000

    _LOGGER.debug("SMA register %s (%s) value: %s", address, name, raw_value)

    return raw_value


async def read_sma_data(hass, host, port):
    """Read SMA inverter data."""

    def _read():
        client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=5,
        )

        try:
            _LOGGER.debug("Connecting to SMA inverter %s:%s", host, port)

            if not client.connect():
                _LOGGER.warning("Could not connect to SMA inverter %s:%s", host, port)
                return {}

            _LOGGER.debug("Connected to SMA inverter %s:%s", host, port)

            data = {
                "current_power": _read_s32(client, 30775, "current_power"),
                "energy_today": _read_s32(client, 30535, "energy_today"),
                "temperature": _read_s32(client, 30953, "temperature"),
            }

            _LOGGER.debug("SMA data read complete: %s", data)

            return data

        except Exception as err:
            _LOGGER.exception("Unexpected error while reading SMA inverter: %r", err)
            return {}

        finally:
            _LOGGER.debug("Closing SMA Modbus connection")
            client.close()

    return await hass.async_add_executor_job(_read)