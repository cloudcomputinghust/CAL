""" OpenstackDriver for Network
    based on BaseDriver
"""


from keystoneauth1.identity import v3
from keystoneauth1 import session
from neutronclient.v2_0 import client

from calplus.v1.network.drivers.base import BaseDriver, BaseQuota


PROVIDER = "OPENSTACK"


class NeutronDriver(BaseDriver):

    """docstring for OpenstackDriver"""

    def __init__(self, cloud_config):
        super(NeutronDriver, self).__init__()
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
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)
        sess = session.Session(auth=auth)
        self.client = client.Client(session=sess)
        self.network_quota = OpenstackQuota(
            self.client, self.tenant_id, self.limit)

    def _check_external_network(self):
        networks = self.client.list_networks().get('networks')
        for network in networks:
            external = network.get('provider:physical_network')
            if external is not None:
                return network.get('id')
        return None

    def _check_router_external_gateway(self):
        routers = self.client.list_routers().get('routers')
        for router in routers:
            external = router.get('external_gateway_info')
            if external is not None:
                return router.get('id')
        return None

    def create(self, name, cidr, **kargs):
        admin_state_up = kargs.pop('admin_state_up', True)
        ip_version = kargs.pop('ip_version', 4)

        # step1: create network with empty name and admin_state_up
        network = {'name': '',
                   'admin_state_up': admin_state_up}
        net = self.client.create_network({'network': network}).get('network')
        network_id = net['id']

        # step 2: create subnet
        sub = {"network_id": network_id,
               "ip_version": ip_version,
               "cidr": cidr,
               "name": name}
        subnet = self.client.create_subnet({'subnet': sub}).get('subnet')

        result = {'name': subnet['name'],
                  'description': None,
                  'id': subnet['id'],
                  'cidr': subnet['cidr'],
                  'cloud': PROVIDER,
                  'gateway_ip': subnet['gateway_ip'],
                  'security_group': None,
                  'allocation_pools': subnet['allocation_pools'],
                  'dns_nameservers': subnet['dns_nameservers']
                  }

        return result

    def show(self, subnet_id):
        subnet = self.client.show_subnet(subnet_id).get('subnet')

        result = {'name': subnet['name'],
                  'description': None,
                  'id': subnet['id'],
                  'cidr': subnet['cidr'],
                  'cloud': PROVIDER,
                  'gateway': subnet['gateway_ip'],
                  'security_group': None,
                  'allocation_pools': subnet['allocation_pools'],
                  'dns_nameservers': subnet['dns_nameservers']
                  }

        return result

    def list(self, **search_opts):
        subnets = self.client.list_subnets(**search_opts).get('subnets')
        result = []
        for subnet in subnets:
            sub = {'name': subnet['name'],
                   'description': None,
                   'id': subnet['id'],
                   'cidr': subnet['cidr'],
                   'cloud': PROVIDER,
                   'gateway': subnet['gateway_ip'],
                   'security_group': None,
                   'allocation_pools': subnet['allocation_pools'],
                   'dns_nameservers': subnet['dns_nameservers']
                   }
            result.append(sub)

        return result

    def update(self, network_id, network):
        # Now we can't update network, I'm trying again
        return None

    def delete(self, network_id):
        return self.client.delete_network(network_id)

    def connect_external_net(self, subnet_id):
        router_id = self._check_router_external_gateway()
        if router_id is None:
            network_id = self._check_external_network()
            if network_id is None:
                raise Exception()
            router = {
                "name": "default",
                "external_gateway_info": {
                    "network_id": "{}".format(network_id)
                }
            }
            router = self.create_router({'router': router})

        body = {
            "subnet_id": "{}".format(subnet_id)
        }
        return self.client.add_interface_router(router_id, body)

    def disconnect_external_net(self, network_id):
        #just detach all connect to router have external_gateway
        pass

    def allocate_public_ip(self):
        external_net = self._check_external_network()
        if external_net:
            create_dict = {'floating_network_id': external_net,
                           'tenant_id': self.network_quota.tenant_id}
            self.client.create_floatingip({'floatingip': create_dict})
        else:
            return False
        return True

    def list_public_ip(self, **search_opts):
        """

        :param search_opts:
        :return: list PublicIP
        """
        result = self.client.list_floatingips(**search_opts)
        ips = result.get('floatingips')
        return_format = []
        for ip in ips:
            return_format.append({
                'public_ip': ip.get('floating_ip_address'),
                'id': ip.get('id')
            })
        return return_format

    def release_public_ip(self, public_ip_id):
        self.client.delete_floatingip(public_ip_id)
        return True


class OpenstackQuota(BaseQuota):

    """docstring for OpenstackQuota"""

    def __init__(self, client, tenant_id=None, limit=None):
        super(OpenstackQuota, self).__init__()
        self.client = client
        self.tenant_id = tenant_id
        self.limit = limit
        self._setup()

    def _setup(self):
        if self.tenant_id is None:
            self.tenant_id = \
                self.client.get_quotas_tenant().get('tenant')['tenant_id']

        if self.limit is None:
            self.limit = self.client.show_quota(self.tenant_id).get('quota')

    def get_networks(self):
        subnets = self.client.list_subnets().get('subnets')
        list_cidrs = []
        for subnet in subnets:
            list_cidrs.append({
                "net_id": subnet['id'],
                "cidr": "{}".format(subnet['cidr']),
                "allocation_pools": subnet['allocation_pools']
            })
        networks = {
            "max": self.limit['network'],
            "used": len(list_cidrs),
            "list_cidrs": list_cidrs,
            "VPCs": None
        }

        return networks

    def get_security_groups(self):
        list_security_groups = self.client.list_security_groups(
            tenant_id=self.tenant_id).get('security_groups')
        list_scgs = []
        for scg in list_security_groups:
            list_scgs.append({
                "security_group_id": scg['id'],
                "rules_max": self.limit['security_group_rule'],
                "rules_used": len(scg['security_group_rules']),
                "list_rules": scg['security_group_rules']
            })
        security_groups = {
            "max": self.limit['security_group'],
            "used": len(list_security_groups),
            "list_security_groups": list_scgs
        }
        return security_groups

    def get_floating_ips(self):
        ips = self.client.list_floatingips().get('floatingips')
        list_ips = []
        for ip in ips:
            list_ips.append(ip['floating_ip_address'])
        floating_ips = {
            "max": self.limit['security_group'],
            "used": len(list_ips),
            "list_floating_ips": list_ips
        }

        return floating_ips

    def get_routers(self):
        rts = self.client.list_routers().get('routers')
        list_routers = []
        for router in rts:
            list_routers.append({
                "router_id": router['id'],
                "is_gateway": True
            })
        routers = {
            "max": self.limit['router'],
            "used": len(list_routers),
            "list_routers": list_routers
        }

        return routers

    def get_internet_gateways(self):
        routers = self.client.list_routers().get('routers')
        internet_gateways = []
        for router in routers:
            egi = router.get('external_gateway_info', None)
            if egi is not None:
                internet_gateways.append({
                    'internet_gateway_id': router['id']
                })

        return internet_gateways
