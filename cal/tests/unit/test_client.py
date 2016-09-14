import mock

import cal.conf
from cal import client
from cal import exceptions
from cal.tests.base import TestCase
# from cal.v1.network import client as network_client

CONF = cal.conf.CONF


class TestClient(TestCase):

    @mock.patch.object(client, 'Client')
    def setUp(self, mock_client):
        super(TestClient, self).setUp()
        self.mock_client = mock_client

    def test_client_called_with_unsupported_provider(self):
        self.assertRaises(exceptions.ProviderNotFound, client.Client,
                          '1.0.0', 'compute', 'WrongProvider')

    # def test_client_called_with_none_provider(self):
    #     test_client = client.Client(version='1.0.0', resource='network')
    #     self.assertIsNotNone(test_client.driver)

    def test_client_called_with_unsupported_version(self):
        self.assertRaises(exceptions.UnsupportedVersion, client.Client,
                          'wrong_version', 'compute', 'OpenStack')

    def test_client_called_with_none_resource(self):
        self.assertRaises(exceptions.ResourceNotDefined, client.Client,
                          '1.0.0', None, 'OpenStack')

    def test_client_called_with_unknow_resource(self):
        self.assertRaises(exceptions.ResourceNotFound, client.Client,
                          '1.0.0', 'wrong_resource', 'OpenStack')
