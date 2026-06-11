import socket

from pymodbus.client import ModbusTcpClient


SMA_UNIT_ID = 3
SMA_INVALID_U32 = 0x80000000


async def test_connection(hass, host, port, timeout=5):
    """Test TCP connection to SMA inverter."""

    def _test():
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    return await hass.async_add_executor_job(_test)


def _read_s32(client, address):
    result = client.read_holding_registers(
        address=address,
        count=2,
        device_id=SMA_UNIT_ID,
    )

    if result.isError() or len(result.registers) < 2:
        return None

    raw_value = (result.registers[0] << 16) + result.registers[1]

    if raw_value == SMA_INVALID_U32:
        return None

    if raw_value >= 0x80000000:
        raw_value -= 0x100000000

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
            if not client.connect():
                return {}

            return {
                "current_power": _read_s32(client, 30775),
                "energy_today": _read_s32(client, 30535),
                "temperature": _read_s32(client, 30953),
            }

        except Exception:
            return {}

        finally:
            client.close()

    return await hass.async_add_executor_job(_read)