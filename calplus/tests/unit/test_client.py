import mock

import calplus.conf
from calplus import client
from calplus import exceptions
from calplus.tests.base import TestCase
from calplus.provider import Provider

CONF = calplus.conf.CONF


fake_aws_auth_opts = {
    'drive_name': 'New AMAZON',
    'type_driver': 'amazon',
    'aws_access_key_id': 'fake_id',
    'aws_secret_access_key': 'fake_key',
    'region_name': 'RegionOne',
    'endpoint_url': 'http://localhost:8788',
    'limit': {
        "subnet": 10,
        "vpc": 5,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}

wrong_driver = Provider('wrong_type', 'fake_config')
right_driver = Provider('openstack', 'fake_config')


class TestClient(TestCase):

    @mock.patch.object(client, 'Client')
    def setUp(self, mock_client):
        super(TestClient, self).setUp()
        self.mock_client = mock_client

    def test_client_called_with_unsupported_provider(self):
        self.assertRaises(exceptions.TypeProviderNotFound, client.Client,
                          '1.0.0', 'compute', wrong_driver)

    def test_client_called_with_none_provider(self):
        self.assertRaises(exceptions.ProviderNotDefined, client.Client,
                          '1.0.0', 'compute')

    def test_client_called_with_unsupported_version(self):
        self.assertRaises(exceptions.UnsupportedVersion, client.Client,
                          'wrong_version', 'compute', right_driver)

    def test_client_called_with_none_resource(self):
        self.assertRaises(exceptions.ResourceNotDefined, client.Client,
                          '1.0.0', None, right_driver)

    def test_client_called_with_unknow_resource(self):
        self.assertRaises(exceptions.ResourceNotFound, client.Client,
                          '1.0.0', 'wrong_resource', right_driver)
