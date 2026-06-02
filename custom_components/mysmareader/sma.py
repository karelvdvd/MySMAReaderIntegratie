import socket

from pymodbus.client import ModbusTcpClient


SMA_UNIT_ID = 3


async def test_connection(hass, host, port, timeout=5):
    """Test TCP connection to SMA inverter."""

    def _test():
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    return await hass.async_add_executor_job(_test)


async def read_current_power(hass, host, port):
    """Read current PV power from SMA inverter."""

    def _read():
        client = ModbusTcpClient(host=host, port=port, timeout=5)

        try:
            if not client.connect():
                return None

            result = client.read_holding_registers(
                address=30775,
                count=2,
                slave=SMA_UNIT_ID,
            )

            if result.isError():
                return None

            registers = result.registers

            value = (registers[0] << 16) + registers[1]

            if value >= 0x80000000:
                value -= 0x100000000

            return value

        finally:
            client.close()

    return await hass.async_add_executor_job(_read)