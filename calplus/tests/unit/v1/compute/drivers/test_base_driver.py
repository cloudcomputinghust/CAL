""" Some test for BaseDriver
"""


from calplus.tests import base
from calplus.v1.compute.drivers.base import BaseDriver


class FakeDriver(BaseDriver):
    """docstring for FakeDriver
        This class implemented all of BaseDriver functions
    """
    def __init__(self):
        super(FakeDriver, self).__init__()

    def create(self, image_id, flavor_id,
               network_id, name=None, number=1, **kargs):
        return 'fake_result'

    def show(self, instance_id):
        return 'fake_result'

    def list(self, **search_opts):
        return 'fake_result'

    def delete(self, instance_id):
        return 'fake_result'

    def shutdown(self, instance_id):
        return 'fake_result'

    def start(self, instance_id):
        return 'fake_result'

    def reboot(self, instance_id):
        return 'fake_result'

    def resize(self, instance_id, configuration):
        return 'fake_result'

    def add_sg(self, instance_id, new_sg):
        """Add a security group"""
        return 'fake_result'

    def delete_sg(self, instance_id, new_sg):
        """Delete a security group"""
        return 'fake_result'

    def list_sg(self, instance_id):
        """List all security group"""
        return 'fake_result'

    def add_nic(self, instance_id, new_sg):
        """Add a Network Interface Controller"""
        return 'fake_result'

    def delete_nic(self, instance_id, new_sg):
        """Delete a Network Interface Controller"""
        return 'fake_result'

    def list_nic(self, instance_id):
        """List all Network Interface Controller"""
        return 'fake_result'

    def add_private_ip(self, instance_id, new_sg):
        """Add private IP"""
        return 'fake_result'

    def delete_private_ip(self, instance_id, new_sg):
        """Delete private IP"""
        return 'fake_result'

    def add_public_ip(self, instance_id, new_sg):
        """Add a external IP"""
        return 'fake_result'

    def delete_public_ip(self, instance_id, new_sg):
        """Delete a external IP"""
        return 'fake_result'

    def list_ip(self, instance_id, new_sg):
        """Add all IPs"""
        return 'fake_result'


class FakeDriverError(BaseDriver):
    """docstring for FakeDriverError
        This class didn't implement some functions
    """
    def __init__(self):
        super(FakeDriverError, self).__init__()

    def create(self, image_id, flavor_id,
               network_id, name=None, number=1, **kargs):
        return 'fake_result'

    def show(self, instance_id):
        return 'fake_result'


class ComputeDriverTest(base.TestCase):

    """Testing class for BaseDriver"""

    def setUp(self):
        super(ComputeDriverTest, self).setUp()

    def test_create_base_driver_object(self):
        fake_driver = FakeDriver()
        self.assertIsInstance(fake_driver, FakeDriver)

    def test_create_base_driver_object_unable_to_create(self):
        self.assertRaises(TypeError, FakeDriverError)
