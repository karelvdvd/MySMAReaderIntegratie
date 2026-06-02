from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL, DOMAIN
from .sma import read_sma_data

_LOGGER = logging.getLogger(__name__)


class MySMADataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator for My SMA Reader."""

    def __init__(self, hass, entry):
        """Initialize coordinator."""
        self.host = entry.data[CONF_HOST]
        self.port = entry.data[CONF_PORT]
        scan_interval = entry.data.get(CONF_SCAN_INTERVAL, 20)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        """Fetch data from SMA inverter."""
        return await read_sma_data(
            self.hass,
            self.host,
            self.port,
        )