""" OpenstackDriver for Compute
    based on BaseDriver
"""


from datetime import datetime
import six

from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client

from calplus.v1.compute.drivers.base import BaseDriver, BaseQuota


PROVIDER = "OPENSTACK"


class OpenstackDriver(BaseDriver):
    """docstring for OpenstackDriver"""

    def __init__(self, cloud_config):
        super(OpenstackDriver, self).__init__()
        self.auth_url = cloud_config['os_auth_url']
        self.project_name = cloud_config['os_project_name']
        self.username = cloud_config['os_username']
        self.password = cloud_config['os_password']
        self.user_domain_name = \
            cloud_config.get('os_project_domain_name', 'default')
        self.project_domain_name = \
            cloud_config.get('os_user_domain_name', 'default')
        self.driver_name = \
            cloud_config.get('driver_name', 'default')
        self.tenant_id = cloud_config.get('tenant_id', None)
        self.limit = cloud_config.get('limit', None)
        self.client_version = \
            cloud_config.get('os_novaclient_version', '2.1')
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)
        sess = session.Session(auth=auth)
        self.client = Client(self.client_version, session=sess)
        self.quota = OpenstackQuota(
            self.client, self.tenant_id, self.limit)

    def create(self, flavor_id,
               network_id, key_name,image_id=None, name=None, block_device_mapping=None, number=1, **kargs):
        if name is None:
            name = six.text_type(datetime.now())
        server = self.client.servers.create(
            name=name,
            image=image_id,
            flavor=flavor_id,
            nics=[{'net-id': network_id}],
            key_name=key_name,
            max_count=number,
            block_device_mapping_v2=block_device_mapping
        )
        return server

    def show(self, instance_id):
        server = self.client.servers.get(
            instance_id
        )
        return server

    def list(self, **search_opts):
        servers = self.client.servers.list(search_opts=search_opts)
        return servers

    def delete(self, instance_id):
        self.client.servers.delete(instance_id)
        return True

    def shutdown(self, instance_id):
        self.client.servers.stop(instance_id)
        return True

    def start(self, instance_id):
        self.client.servers.start(instance_id)
        return True

    def reboot(self, instance_id):
        """Soft reboot"""
        self.client.servers.reboot(instance_id)
        return True

    def resize(self, instance_id, flavor_id):
        self.client.servers.resize(instance_id, flavor_id)
        try:
            self.client.servers.confirm_resize(instance_id)
        except:
            self.client.servers.revert_resize(instance_id)
            return False
        return True

    def add_sg(self, instance_id, new_sg):
        """Add a security group"""
        pass

    def delete_sg(self, instance_id, new_sg):
        """Delete a security group"""
        pass

    def list_sg(self, instance_id):
        """List all security group"""
        pass

    def add_nic(self, instance_id, net_id):
        """Add a Network Interface Controller"""
        #TODO: upgrade with port_id and fixed_ip in future
        self.client.servers.interface_attach(
            instance_id, None, net_id, None)
        return True

    def delete_nic(self, instance_id, port_id):
        """Delete a Network Interface Controller"""
        self.client.servers.interface_detach(instance_id, port_id)
        return True

    def list_nic(self, instance_id):
        """List all Network Interface Controller
        """
        #NOTE: interfaces a list of novaclient.v2.servers.Server
        interfaces = self.client.servers.interface_list(instance_id)
        return interfaces

    def add_private_ip(self, instance_id, new_sg):
        """Add private IP"""
        pass

    def delete_private_ip(self, instance_id, new_sg):
        """Delete private IP"""
        pass

    def associate_public_ip(self, instance_id, public_ip_id, private_ip=None):
        """Associate a external IP"""
        floating_ip = self.client.floating_ips.get(public_ip_id)
        floating_ip = floating_ip.to_dict()
        address = floating_ip.get('ip')

        self.client.servers.add_floating_ip(instance_id, address, private_ip)

        return True

    def disassociate_public_ip(self, public_ip_id):
        """Disassociate a external IP"""
        floating_ip = self.client.floating_ips.get(public_ip_id)
        floating_ip = floating_ip.to_dict()
        instance_id = floating_ip.get('instance_id')
        address = floating_ip.get('ip')

        self.client.servers.remove_floating_ip(instance_id, address)

        return True

    def list_ip(self, instance_id):
        """Add all IPs"""
        return dict(self.client.servers.ips(instance_id))


class OpenstackQuota(BaseQuota):
    """docstring for OpenStack Compute Quota"""
    def __init__(self, client, tenant_id=None, limit=None):
        super(OpenstackQuota, self).__init__()
        self.client = client
        self.tenant_id = tenant_id
        self.limit = limit
        self._setup()

    def _setup(self):
        pass

    def get_vcpus(self):
        pass

    def get_instances(self):
        pass

    def get_ram(self):
        pass
