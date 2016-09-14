import cal.conf
from cal.base import BaseClient

CONF = cal.conf.CONF


class Client(BaseClient):
    """Top-level object to access CAL API
    This class must be extended base.Singleton class to make
    sure only one instance of this one is ever created."""

    def __init__(self, provider, cloud_config, *args, **kwargs):
        BaseClient.__init__(self, CONF.network.driver_path,
                            provider, cloud_config)

    def create(self, name, cidr, **kwargs):
        """This function will create a user network.
        Within OpenStack, it will create a network and a subnet
        Within AWS, it will create a VPC and a subnet

        :param name: string
        :param cidr: string E.x: "10.0.0.0/24"
        :param kwargs: dict
        :return: dict
        """
        return self.driver.create(name, cidr, **kwargs)

    def delete(self, network_id):
        """Delete a network.

        :param network_id: string
        - Within OpenStack: network id
        - Within AWS: VPC id
        :return:
        """
        return self.driver.delete(network_id)

    def list(self, **search_opts):
        return self.driver.list(**search_opts)

    def show(self, subnet_id):
        return self.driver.show(subnet_id)

    def update(self, network_id, network):
        return self.driver.update(network_id, network)
