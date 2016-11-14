""" AmazonDriver for Network
    based on BaseDriver for Network Resource
"""


import mock

from botocore.exceptions import ClientError

from calplus.tests import base
from calplus.v1.network.drivers.amazon import AmazonDriver


fake_config_driver = {
    'aws_access_key_id': 'c543fa29eeaf4894a1078ec0860baefd',
    'aws_secret_access_key': 'd2246a2235ca40ffa7fbf817ae1108ba',
    'region_name': 'RegionOne',
    'endpoint_url': 'http://192.168.122.75:8788'
}

fake_vpc_out = {
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RequestId': 'req-0b7db2b4-420e-4217-9106-e8cdb4137f65',
        'HTTPHeaders': {
            'date': 'Tue, 13 Sep 2016 09:52:24 GMT',
            'content-length': '351',
            'content-type': 'text/xml'
        }
    },
    'Vpc': {
        'State': 'available',
        'VpcId': 'vpc-5eed72c5',
        'CidrBlock': '10.10.10.0/24',
        'IsDefault': False,
        'DhcpOptionsId': 'default'
    }
}

fake_subnet_out = {
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RequestId': 'req-261a0331-1d6a-4bfc-92b1-5de9178cdf85',
        'HTTPHeaders': {
            'date': 'Tue, 13 Sep 2016 10:25:20 GMT',
            'content-length': '479',
            'content-type': 'text/xml'
        }
    },
    'Subnet': {
        'VpcId': 'vpc-5eed72c5',
        'CidrBlock': '10.10.10.0/24',
        'DefaultForAz': False,
        'State': 'available',
        'MapPublicIpOnLaunch': False,
        'SubnetId': 'subnet-9dcb6b38',
        'AvailableIpAddressCount': 252
    }
}

fake_describe_subnets = {
    'Subnets': [{
        'VpcId': 'vpc-5eed72c5',
        'CidrBlock': '10.10.10.0/24',
        'DefaultForAz': False,
        'State': 'available',
        'MapPublicIpOnLaunch': False,
        'SubnetId': 'subnet-9dcb6b38',
        'AvailableIpAddressCount': 252
    }],
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RequestId': 'req-51a26aea-2fd6-47df-99ab-adeb5c69c01a',
        'HTTPHeaders': {
            'date': 'Fri, 23 Sep 2016 22:53:46 GMT',
            'content-length': '528',
            'content-type': 'text/xml'
        }
    }
}

fake_delete_subnet_out = {
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RequestId':
        'req-6bab2f81-a4fa-4089-958c-380f563644d2',
        'HTTPHeaders': {
            'date': 'Fri, 23 Sep 2016 23:25:15 GMT',
            'content-length': '186',
            'content-type': 'text/xml'
        }
    }
}

fake_delete_vpc_out = {
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RequestId': 'req-df29f045-aff2-42fe-bab6-d1fd0d9cf45b',
        'HTTPHeaders': {
            'date': 'Fri, 23 Sep 2016 23:32:40 GMT',
            'content-length': '180',
            'content-type':
            'text/xml'
        }
    }
}

fake_error_code = {
    'ResponseMetadata': {
        'HTTPStatusCode': 400,
        'RequestId': 'req-a4570d1a-8319-4d6f-8077-7044d72ef449',
        'HTTPHeaders': {
            'date': 'Sat, 24 Sep 2016 03:09:39 GMT',
            'content-length': '250',
            'content-type': 'text/xml'
        }
    },
    'Error': {
        'Message': "The subnet ID 'fake_id' does not exist",
        'Code': 'InvalidSubnetID.NotFound'
    }
}

fake_allocate_ip_out = {
    'PublicIp': '192.168.122.224',
    'Domain': 'vpc',
    'AllocationId': 'eipalloc-8f665a3d',
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RequestId': 'req-df29f045-aff2-42fe-bab6-d1fd0d9cf45b',
        'HTTPHeaders': {
            'date': 'Fri, 23 Sep 2016 23:32:40 GMT',
            'content-length': '180',
            'content-type':
            'text/xml'
        }
    }
}


class AmazonDriverTest(base.TestCase):

    """docstring for AmazonDriverTest"""

    def setUp(self):
        super(AmazonDriverTest, self).setUp()
        self.fake_driver = AmazonDriver(fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'create_vpc',
            mock.Mock(return_value=fake_vpc_out))
        self.mock_object(
            self.fake_driver.client, 'create_subnet',
            mock.Mock(return_value=fake_subnet_out))
        self.fake_driver.create('fake_name', '10.10.10.0/24')

        self.fake_driver.client.create_vpc.\
            assert_called_once_with(
                CidrBlock='10.10.10.0/24',
                InstanceTenancy='default'
            )
        self.fake_driver.client.create_subnet.\
            assert_called_once_with(
                VpcId='vpc-5eed72c5',
                CidrBlock='10.10.10.0/24'
            )

    def test_create_unable_to_create_vpc(self):
        self.mock_object(
            self.fake_driver.client, 'create_vpc',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )
            )
        )
        self.mock_object(
            self.fake_driver.client, 'create_subnet', mock.Mock())

        self.assertRaises(ClientError, self.fake_driver.create,
                          'fake_name', '10.10.10.0/24')

        self.fake_driver.client.create_vpc.\
            assert_called_once_with(
                CidrBlock='10.10.10.0/24',
                InstanceTenancy='default'
            )
        self.assertFalse(self.fake_driver.client.create_subnet.called)

    def test_create_unable_to_create_subnet(self):
        self.mock_object(
            self.fake_driver.client, 'create_vpc',
            mock.Mock(return_value=fake_vpc_out))
        self.mock_object(
            self.fake_driver.client, 'create_subnet',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )))

        self.assertRaises(ClientError, self.fake_driver.create,
                          'fake_name', '10.10.10.0/24')

        self.fake_driver.client.create_vpc.\
            assert_called_once_with(
                CidrBlock='10.10.10.0/24',
                InstanceTenancy='default'
            )
        self.fake_driver.client.create_subnet.\
            assert_called_once_with(
                VpcId='vpc-5eed72c5',
                CidrBlock='10.10.10.0/24'
            )

    def test_show_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(return_value=fake_describe_subnets))
        self.fake_driver.show('subnet-9dcb6b38')

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with(SubnetIds=['subnet-9dcb6b38'])

    def test_show_unable_to_show_network(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )))

        self.assertRaises(ClientError, self.fake_driver.show,
                          'subnet-9dcb6b38')

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with(SubnetIds=['subnet-9dcb6b38'])

    def test_list_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(return_value=fake_describe_subnets))

        self.fake_driver.list()

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with()

    def test_list_unable_to_list_network(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )
            )
        )

        self.assertRaises(ClientError, self.fake_driver.list)

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with()

    def test_update_successfully(self):
        self.fake_driver.update('fake_id', fake_subnet_out)

    def test_update_unable_to_update_network(self):
        pass

    def test_delete_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(return_value=fake_describe_subnets))
        self.mock_object(
            self.fake_driver.client, 'delete_subnet',
            mock.Mock(return_value=fake_delete_subnet_out))
        self.mock_object(
            self.fake_driver.client, 'delete_vpc',
            mock.Mock(return_value=fake_delete_vpc_out))

        self.fake_driver.delete('subnet-9dcb6b38')

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with(SubnetIds=['subnet-9dcb6b38'])
        self.fake_driver.client.delete_subnet.\
            assert_called_once_with(SubnetId='subnet-9dcb6b38')
        self.fake_driver.client.delete_vpc.\
            assert_called_once_with(VpcId='vpc-5eed72c5')

    def test_delete_unable_to_describe_subnets(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )
            ))
        self.mock_object(self.fake_driver.client,
            'delete_subnet', mock.Mock())
        self.mock_object(self.fake_driver.client,
                         'delete_vpc', mock.Mock())

        self.assertRaises(ClientError, self.fake_driver.delete,
                          'subnet-9dcb6b38')

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with(SubnetIds=['subnet-9dcb6b38'])
        self.assertFalse(self.fake_driver.client.delete_subnet.called)
        self.assertFalse(self.fake_driver.client.delete_vpc.called)

    def test_delete_unable_to_detete_subnet(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(return_value=fake_describe_subnets))
        self.mock_object(
            self.fake_driver.client, 'delete_subnet',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )
            ))
        self.mock_object(
            self.fake_driver.client, 'delete_vpc', mock.Mock())

        self.assertRaises(ClientError, self.fake_driver.delete,
                          'subnet-9dcb6b38')

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with(SubnetIds=['subnet-9dcb6b38'])
        self.fake_driver.client.delete_subnet.\
            assert_called_once_with(SubnetId='subnet-9dcb6b38')
        self.assertFalse(self.fake_driver.client.delete_vpc.called)

    def test_delete_unable_to_detete_vpc(self):
        self.mock_object(
            self.fake_driver.client, 'describe_subnets',
            mock.Mock(return_value=fake_describe_subnets))
        self.mock_object(
            self.fake_driver.client, 'delete_subnet',
            mock.Mock(return_value=fake_delete_subnet_out))
        self.mock_object(
            self.fake_driver.client, 'delete_vpc',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )
            ))

        self.assertRaises(ClientError, self.fake_driver.delete,
                          'subnet-9dcb6b38')

        self.fake_driver.client.describe_subnets.\
            assert_called_once_with(SubnetIds=['subnet-9dcb6b38'])
        self.fake_driver.client.delete_subnet.\
            assert_called_once_with(SubnetId='subnet-9dcb6b38')
        self.fake_driver.client.delete_vpc.\
            assert_called_once_with(VpcId='vpc-5eed72c5')

    def test_allocate_public_ip_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'allocate_address',
            mock.Mock(return_value=fake_allocate_ip_out))

        self.fake_driver.allocate_public_ip()

        self.fake_driver.client.allocate_address.\
            assert_called_once_with(Domain='vpc')

    def test_allocate_public_ip_unable_to_allocate(self):
        self.mock_object(
            self.fake_driver.client, 'allocate_address',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )
            )
        )

        self.assertRaises(ClientError,
                          self.fake_driver.allocate_public_ip)

        self.fake_driver.client.allocate_address.\
            assert_called_once_with(Domain='vpc')
