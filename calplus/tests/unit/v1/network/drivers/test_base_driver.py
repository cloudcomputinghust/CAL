""" Some test for BaseDriver
"""


from calplus.tests import base
from calplus.v1.network.drivers.base import BaseDriver


class FakeDriver(BaseDriver):
    """docstring for FakeDriver
        This class implemented all of BaseDriver functions
    """
    def __init__(self):
        super(FakeDriver, self).__init__()

    def create(self, name, cidr, **kargs):
        return 'fake_result'

    def show(self, subnet_id):
        return 'fake_result'

    def list(self, **search_opts):
        return 'fake_result'

    def update(self, network_id, network):
        return 'fake_result'

    def delete(self, network_id):
        return 'fake_result'

    def connect_external_net(self, network_id):
        return 'fake_result'

    def disconnect_external_net(self, network_id):
        return 'fake_result'

    def allocate_public_ip(self, network_id):
        return 'fake_result'

    def list_public_ip(self, **search_opts):
        return 'fake_result'


class FakeDriverError(BaseDriver):
    """docstring for FakeDriverError
        This class didn't implement some functions
    """
    def __init__(self):
        super(FakeDriverError, self).__init__()

    def create(self, name, cidr, **kargs):
        return 'fake_result'

    def show(self, subnet_id):
        return 'fake_result'

    def list(self, **search_opts):
        return 'fake_result'

    def update(self, network_id, network):
        return 'fake_result'

    def connect_external_net(self, network_id):
        return 'fake_result'

    def disconnect_external_net(self, network_id):
        return 'fake_result'


class NetWorkDriverTest(base.TestCase):

    """Testing class for BaseDriver"""

    def setUp(self):
        super(NetWorkDriverTest, self).setUp()

    def test_create_base_driver_object(self):
        fake_driver = FakeDriver()
        self.assertIsInstance(fake_driver, FakeDriver)

    def test_create_base_driver_object_unable_to_create(self):
        self.assertRaises(TypeError, FakeDriverError)
