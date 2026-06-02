import socket


async def test_connection(hass, host, port, timeout=5):
    """Test TCP connection to SMA inverter."""

    def _test():
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    return await hass.async_add_executor_job(_test)