import mock
from keystoneauth1.exceptions.base import ClientException

from calplus.tests import base
from calplus.v1.network import client


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


class ClientTest(base.TestCase):

    """docstring for ClientTest"""

    def setUp(self):
        super(ClientTest, self).setUp()
        self.fake_client = client.Client(
            'OpenStack', fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'create',
            mock.Mock(return_value={
                'network': fake_network_out
            }))

        self.fake_client.create('fake_name', 'fake_cidr')

        self.fake_client.driver.create.\
            assert_called_once_with('fake_name', 'fake_cidr')

    def test_create_unable_to_create(self):
        self.mock_object(
            self.fake_client.driver, 'create',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.create, 'fake_name', 'fake_cidr')

        self.fake_client.driver.create.\
            assert_called_once_with('fake_name', 'fake_cidr')

    def test_delete_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'delete',
            mock.Mock(return_value={}))

        self.fake_client.delete('fake_id')

        self.fake_client.driver.delete.\
            assert_called_once_with('fake_id')

    def test_delete_unable_to_delete(self):
        self.mock_object(
            self.fake_client.driver, 'delete',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.delete, 'fake_id')

        self.fake_client.driver.delete.\
            assert_called_once_with('fake_id')

    def test_list_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'list',
            mock.Mock(return_value={
                'subnets': [fake_subnet_out]
            }))

        self.fake_client.list()

        self.fake_client.driver.list.\
            assert_called_once_with()

    def test_list_unable_to_list(self):
        self.mock_object(
            self.fake_client.driver, 'list',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.list)

        self.fake_client.driver.list.\
            assert_called_once_with()

    def test_show_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'show',
            mock.Mock(return_value={
                'subnet': fake_subnet_out
            }))

        self.fake_client.show('fake_id')

        self.fake_client.driver.show.\
            assert_called_once_with('fake_id')

    def test_show_unable_to_show(self):
        self.mock_object(
            self.fake_client.driver, 'show',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.show, 'fake_id')

        self.fake_client.driver.show.\
            assert_called_once_with('fake_id')

    def test_update_successfully(self):
        self.fake_client.update('fake_id', fake_subnet_out)

    def test_update_unable_to_update(self):
        pass

    def test_connect_external_net_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'connect_external_net',
            mock.Mock(return_value=None))
        #TODO: alter None with exact return format

        self.fake_client.connect_external_net('fake_id')

        self.fake_client.driver.connect_external_net.\
            assert_called_once_with('fake_id')

    def test_connect_external_net_unable_to_connect(self):
        self.mock_object(
            self.fake_client.driver, 'connect_external_net',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.connect_external_net, 'fake_id')

        self.fake_client.driver.connect_external_net.\
            assert_called_once_with('fake_id')

    def test_disconnect_external_net_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'disconnect_external_net',
            mock.Mock(return_value=None))
        #TODO: alter None with exact return format

        self.fake_client.disconnect_external_net('fake_id')

        self.fake_client.driver.disconnect_external_net.\
            assert_called_once_with('fake_id')

    def test_disconnect_external_net_unable_to_disconnect(self):
        self.mock_object(
            self.fake_client.driver, 'disconnect_external_net',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.disconnect_external_net, 'fake_id')

        self.fake_client.driver.disconnect_external_net.\
            assert_called_once_with('fake_id')

    def test_allocate_public_ip_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'allocate_public_ip',
            mock.Mock(return_value=True))

        self.fake_client.allocate_public_ip()

        self.fake_client.driver.allocate_public_ip.\
            assert_called_once_with()

    def test_allocate_public_ip_unable_to_allocate(self):
        self.mock_object(
            self.fake_client.driver, 'allocate_public_ip',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.allocate_public_ip)

        self.fake_client.driver.allocate_public_ip.\
            assert_called_once_with()

    def test_list_public_ip_successfully(self):
        self.mock_object(
            self.fake_client.driver, 'list_public_ip',
            mock.Mock(return_value='fake_list_ip'))

        self.fake_client.list_public_ip()

        self.fake_client.driver.list_public_ip.\
            assert_called_once_with()

    def test_list_public_ip_unable_to_list(self):
        self.mock_object(
            self.fake_client.driver, 'list_public_ip',
            mock.Mock(side_effect=ClientException))

        self.assertRaises(ClientException,
            self.fake_client.list_public_ip)

        self.fake_client.driver.list_public_ip.\
            assert_called_once_with()
