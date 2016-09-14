""" OpenstackDriver for Network
    based on NetworkDriver
"""


import mock
from cal.tests import base
from keystoneauth1.exceptions.base import ClientException
from cal.v1.network.drivers.openstack import OpenstackDriver

fake_config_driver = {
    'os_auth_url': 'http://controller:5000/v2_0',
    'os_username': 'test',
    'os_password': 'veryhard',
    'os_project_name': 'demo',
    'os_endpoint_url': 'http://controller:9696',
    'os_driver_name': 'default',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'tenant_id': 'fake_tenant_id',
    'limit': {
        "subnet": 10,
        "network": 10,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}

fake_network_in = {
    'name': '',
    'admin_state_up': True
}

fake_network_out = {
    'id': 'fake_id'
}

fake_subnet_int = {
    "network_id": 'fake_id',
    "ip_version": 4,
    "cidr": 'fake_cidr',
    "name": 'fake_name'
}

fake_subnet_out = {
    'name': 'fake_name',
    'description': None,
    'id': 'fake_id',
    'cidr': 'fake_cidr',
    'cloud': 'OPENSTACK',
    'gateway_ip': 'fake_gateway_ip',
    'security_group': None,
    'allocation_pools': 'fake_name_allocation_pools',
    'dns_nameservers': 'fake_dns_nameservers',
    "allocation_pools": [
        {
            "start": "192.0.0.2",
            "end": "192.255.255.254"
        }
    ]
}

fake_router = [
    {
        'id': 'fake_router_id1',
        'external_gateway_info': {
            'fake_attr': None
        }
    },
    {
        'id': 'fake_router_id1',
        'external_gateway_info': None
    }
]

fake_security_groups = {
    'id': 'fake_scg_id',
    'security_group_rules': []
}


class OpenstackDriverTest(base.TestCase):

    """docstring for OpenstackDriverTest"""

    def setUp(self):
        super(OpenstackDriverTest, self).setUp()
        self.fake_driver = OpenstackDriver(fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'create_network',
            mock.Mock(return_value={
                'network': fake_network_out
            }))
        self.mock_object(
            self.fake_driver.client, 'create_subnet',
            mock.Mock(return_value={
                'subnet': fake_subnet_out
            }))
        self.fake_driver.create('fake_name', 'fake_cidr')

        self.fake_driver.client.create_network.\
            assert_called_once_with({'network': fake_network_in})
        self.fake_driver.client.create_subnet.\
            assert_called_once_with({'subnet': fake_subnet_int})

    def test_create_unable_to_create_network(self):
        self.mock_object(
            self.fake_driver.client, 'create_network',
            mock.Mock(side_effect=ClientException))
        self.mock_object(
            self.fake_driver.client, 'create_subnet', mock.Mock())

        self.assertRaises(ClientException, self.fake_driver.create,
                          'fake_name', 'fake_cidr')

        self.fake_driver.client.create_network.\
            assert_called_once_with({'network': fake_network_in})
        self.assertFalse(self.fake_driver.client.create_subnet.called)

    def test_create_unable_to_create_subnet(self):
        self.mock_object(
            self.fake_driver.client, 'create_network',
            mock.Mock(return_value={
                'network': fake_network_out
            }))
        self.mock_object(
            self.fake_driver.client, 'create_subnet',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.create,
                          'fake_name', 'fake_cidr')

        self.fake_driver.client.create_network.\
            assert_called_once_with({'network': fake_network_in})
        self.fake_driver.client.create_subnet.\
            assert_called_once_with({'subnet': fake_subnet_int})

    def test_show_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'show_subnet',
            mock.Mock(return_value={
                'subnet': fake_subnet_out
            }))
        self.fake_driver.show('fake_id')

        self.fake_driver.client.show_subnet.\
            assert_called_once_with('fake_id')

    def test_show_unable_to_show_network(self):
        self.mock_object(
            self.fake_driver.client, 'show_subnet',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.show,
                          'fake_id')

        self.fake_driver.client.show_subnet.\
            assert_called_once_with('fake_id')

    def test_list_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(return_value={
                'subnets': [fake_subnet_out]
            }))

        self.fake_driver.list()

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_list_unable_to_list_network(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.list)

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_update_successfully(self):
        self.fake_driver.update('fake_id', fake_subnet_out)

    def test_update_unable_to_update_network(self):
        pass

    def test_delete_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'delete_network',
            mock.Mock(return_value=()))

        self.fake_driver.delete('fake_network_id')

        self.fake_driver.client.delete_network.\
            assert_called_once_with('fake_network_id')

    def test_delete_unable_to_detete_network(self):
        self.mock_object(
            self.fake_driver.client, 'delete_network',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException, self.fake_driver.delete,
                          'fake_network_id')

        self.fake_driver.client.delete_network.\
            assert_called_once_with('fake_network_id')

    def test_setup_tenant_id_and_limit_are_None(self):
        self.fake_driver.network_quota.tenant_id = None
        self.fake_driver.network_quota.limit = None
        self.mock_object(
            self.fake_driver.network_quota.client, 'get_quotas_tenant',
            mock.Mock(return_value={
                'tenant': {
                    'tenant_id': 'fake_tenant_id'
                }
            }))
        self.mock_object(
            self.fake_driver.network_quota.client, 'show_quota',
            mock.Mock(return_value={
                'quota': fake_config_driver['limit']
            }))

        self.fake_driver.network_quota._setup()

        self.fake_driver.network_quota.client.get_quotas_tenant.\
            assert_called_once_with()
        self.fake_driver.network_quota.client.show_quota.\
            assert_called_once_with('fake_tenant_id')

    def test_get_networks(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(return_value={
                'subnets': [fake_subnet_out]
            }))

        self.fake_driver.network_quota.get_networks()

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_get_networks_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_subnets',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_networks)

        self.fake_driver.client.list_subnets.\
            assert_called_once_with()

    def test_get_security_groups_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_security_groups',
            mock.Mock(return_value={
                'security_groups': [fake_security_groups]
            }))

        self.fake_driver.network_quota.get_security_groups()

        self.fake_driver.client.list_security_groups.\
            assert_called_once_with(tenant_id='fake_tenant_id')

    def test_get_security_groups_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_security_groups',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_security_groups)

        self.fake_driver.client.list_security_groups.\
            assert_called_once_with(tenant_id='fake_tenant_id')

    def test_get_floating_ips(self):
        self.mock_object(
            self.fake_driver.client, 'list_floatingips',
            mock.Mock(return_value={
                'floatingips': [
                    {'floating_ip_address': '192.168.50.238'},
                    {'floating_ip_address': '192.168.50.239'}
                ]
            }))

        self.fake_driver.network_quota.get_floating_ips()

        self.fake_driver.client.list_floatingips.\
            assert_called_once_with()

    def test_get_floating_ips_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_floatingips',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_floating_ips)

        self.fake_driver.client.list_floatingips.\
            assert_called_once_with()

    def test_get_routers(self):
        self.mock_object(
            self.fake_driver.client, 'list_routers',
            mock.Mock(return_value={
                'routers': fake_router
            }))

        self.fake_driver.network_quota.get_routers()

        self.fake_driver.client.list_routers.\
            assert_called_once_with()

    def test_get_routers_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_routers',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_routers)

        self.fake_driver.client.list_routers.\
            assert_called_once_with()

    def test_get_internet_gateways(self):
        self.mock_object(
            self.fake_driver.client, 'list_routers',
            mock.Mock(return_value={
                'routers': fake_router
            }))

        self.fake_driver.network_quota.get_internet_gateways()

        self.fake_driver.client.list_routers.\
            assert_called_once_with()

    def test_get_internet_gateways_unable_to_get_quota(self):
        self.mock_object(
            self.fake_driver.client, 'list_routers',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
                          self.fake_driver.network_quota.get_internet_gateways)

        self.fake_driver.client.list_routers.\
            assert_called_once_with()
