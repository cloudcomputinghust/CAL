""" this is contain Abstract Class and Quota Class
    for all network driver which we want to implement.
"""

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):
    """abstract class for compute driver"""

    def __init__(self):
        super(BaseDriver, self).__init__()

    @abc.abstractmethod
    def create(self, image, flavor,
               network_id, name, number, **kargs):
        pass

    @abc.abstractmethod
    def show(self, instance_id):
        pass

    @abc.abstractmethod
    def list(self, **search_opts):
        pass

    @abc.abstractmethod
    def delete(self, instance_id):
        pass

    @abc.abstractmethod
    def shutdown(self, instance_id):
        pass

    @abc.abstractmethod
    def start(self, instance_id):
        pass

    @abc.abstractmethod
    def reboot(self, instance_id):
        pass

    @abc.abstractmethod
    def resize(self, instance_id, configuration):
        pass

    @abc.abstractmethod
    def add_sg(self, instance_id, new_sg):
        """Add a security group"""
        pass

    @abc.abstractmethod
    def delete_sg(self, instance_id, new_sg):
        """Delete a security group"""
        pass

    @abc.abstractmethod
    def list_sg(self, instance_id):
        """List all security group"""
        pass

    @abc.abstractmethod
    def add_nic(self, instance_id, new_sg):
        """Add a Network Interface Controller"""
        pass

    @abc.abstractmethod
    def delete_nic(self, instance_id, new_sg):
        """Delete a Network Interface Controller"""
        pass

    @abc.abstractmethod
    def list_nic(self, instance_id):
        """List all Network Interface Controller"""
        pass

    @abc.abstractmethod
    def add_private_ip(self, instance_id, new_sg):
        """Add private IP"""
        pass

    @abc.abstractmethod
    def delete_private_ip(self, instance_id, new_sg):
        """Delete private IP"""
        pass

    # @abc.abstractmethod
    # def associate_public_ip(self, instance_id, public_ip_id, private_ip=None):
    #     """Associate a external IP"""
    #     pass

    @abc.abstractmethod
    def disassociate_public_ip(self, public_ip_id):
        """Disassociate a external IP"""
        pass

    @abc.abstractmethod
    def list_ip(self, instance_id):
        """Add all IPs"""
        pass


class BaseQuota(object):
    """docstring for QuotaNetwork"""

    def __init__(self):
        super(BaseQuota, self).__init__()

    def get(self):
        """Get quota from Cloud Provider."""

        # get all network quota from Cloud Provider.
        #TODO: We need to improve this by survey for compute quota
        attrs = ("vcpus",
                 "instances",
                 "ram")

        for attr in attrs:
            setattr(self, attr, eval("self.get_{}()".format(attr)))

    def set(self, attr, value):
        """Update quota for Network."""

        # set special attribute.
        setattr(self, attr, value)

    def get_vcpus(self):
        pass

    def get_instances(self):
        pass

    def get_ram(self):
        pass
