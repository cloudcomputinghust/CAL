""" this is contain Abstract Class and Quota Class
    for all network driver which we want to implement.
"""


import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):
    """abstract class for network driver"""

    def __init__(self):
        super(BaseDriver, self).__init__()
        self.network_quota = BaseQuota()

    @abc.abstractmethod
    def create(self, name, cidr, **kargs):
        pass

    @abc.abstractmethod
    def delete(self, network_id):
        pass

    @abc.abstractmethod
    def list(self, **search_opts):
        pass

    @abc.abstractmethod
    def show(self, subnet_id):
        pass

    @abc.abstractmethod
    def update(self, network_id, network):
        pass

    @abc.abstractmethod
    def connect_external_net(self, network_id):
        pass

    @abc.abstractmethod
    def disconnect_external_net(self, network_id):
        pass

    @abc.abstractmethod
    def allocate_public_ip(self, network_id):
        pass

    @abc.abstractmethod
    def list_public_ip(self, **search_opts):
        pass


class BaseQuota(object):
    """docstring for QuotaNetwork"""
    def __init__(self):
        super(BaseQuota, self).__init__()

    def get(self):
        """Get quota from Cloud Provider."""

        # get all network quota from Cloud Provider.
        attrs = ("networks",
                "security_groups",
                "floating_ips",
                "routers",
                "internet_gateways")

        for attr in attrs:
            setattr(self, attr, eval("self.get_{}()". format(attr)))

    def set(self, attr, value):
        """Update quota for Network."""

        # set special attribute.
        setattr(self, attr, value)

    def get_networks(self):
        pass

    def get_security_groups(self):
        pass

    def get_floating_ips(self):
        pass

    def get_routers(self):
        pass

    def get_internet_gateways(self):
        pass
