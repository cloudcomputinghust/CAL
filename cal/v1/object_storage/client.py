import cal.conf
from cal.base import BaseClient

CONF = cal.conf.CONF


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, cloud_config, *args, **kwargs):
        BaseClient.__init__(self, CONF.object_storage.driver_path,
                            provider, cloud_config)
