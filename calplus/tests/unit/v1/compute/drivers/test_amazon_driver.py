""" AmazonDriver for Compute
    based on BaseDriver for Compute Resource
"""


import mock

from botocore.exceptions import ClientError

from calplus.tests import base
from calplus.v1.compute.drivers.amazon import AmazonDriver


fake_config_driver = {
    'driver_name': 'AMAZON1',
    'aws_access_key_id': 'fake_id',
    'aws_secret_access_key': 'fake_key',
    'region_name': 'us-east-1',
    'endpoint_url': 'http://localhost:8788',
    'limit': {
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

fake_describe_return = {
    'Reservations': [
        {
            'Groups': [],
            'Instances': [
                {
                    'AmiLaunchIndex': 0,
                    'ImageId': 'ami-2624df94',
                    'InstanceId': 'i-72827591',
                    'InstanceType': 'm1.ec2api-alt',
                    'KernelId': 'aki-512bee3f',
                    'KeyName': '',
                    'LaunchTime': 'fake_time',
                    'NetworkInterfaces': [
                        {
                            'Attachment': {
                                'AttachTime': 'fake_time',
                                'AttachmentId': 'eni-attach-ce1477aa',
                                'DeleteOnTermination': True,
                                'DeviceIndex': 0,
                                'Status': 'attached'
                            },
                            'Description': '',
                            'Groups': [
                                {
                                    'GroupId': 'sg-9ed2e7ec',
                                    'GroupName': 'default'
                                }
                            ],
                            'MacAddress': 'fa:16:3e:27:af:a2',
                            'NetworkInterfaceId': 'eni-ce1477aa',
                            'OwnerId': '3b91bb4e974a4729b3596f8cebb9b559',
                            'PrivateIpAddress': '10.10.10.76',
                            'PrivateIpAddresses': [
                                {
                                    'Primary': True,
                                    'PrivateIpAddress': '10.10.10.76'
                                }
                            ],
                            'SourceDestCheck': True,
                            'Status': 'in-use',
                            'SubnetId': 'subnet-b3a91954',
                            'VpcId': 'vpc-9ed2e7ec'
                        }
                    ],
                    'Placement': {
                        'AvailabilityZone': ''
                    },
                    'PrivateDnsName': 'r-atxu9l73-0',
                    'PrivateIpAddress': '10.10.10.76',
                    'PublicDnsName': '',
                    'RamdiskId': 'ari-b7e05ed6',
                    'RootDeviceName': '/dev/vda',
                    'RootDeviceType': 'instance-store',
                    'SecurityGroups': [
                        {
                            'GroupId': 'sg-9ed2e7ec',
                            'GroupName': 'default'
                        }
                    ],
                    'SourceDestCheck': True,
                    'State': {
                        'Code': 0,
                        'Name': 'error'
                    },
                    'SubnetId': 'subnet-b3a91954',
                    'VpcId': 'vpc-9ed2e7ec'
                }
            ],
            'OwnerId': '3b91bb4e974a4729b3596f8cebb9b559',
            'ReservationId': 'r-atxu9l73'
        }
    ],
    'ResponseMetadata': {
        'HTTPHeaders': {
            'content-length': '2971',
            'content-type': 'text/xml',
            'date': 'Wed, 07 Dec 2016 16:17:11 GMT'
        },
        'HTTPStatusCode': 200,
        'RequestId': 'req-646be08c-9104-4855-a0d9-62013ba9566d'
    }
}


class FakeInstance(object):
    """In fact, this class is boto3.resources.factory.ec2.Instance
    """
    def __init__(self):
        super(FakeInstance, self).__init__()

    def terminate(self):
        pass

    def stop(self):
        pass

    def start(self):
        pass

    def reboot(self):
        pass


class AmazonDriverTest(base.TestCase):

    """docstring for AmazonDriverTest"""

    def setUp(self):
        super(AmazonDriverTest, self).setUp()
        self.fake_driver = AmazonDriver(fake_config_driver)

    def test_create_successfully(self):
        self.mock_object(
            self.fake_driver.resource, 'create_instances',
            mock.Mock(return_value=mock.Mock))

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id',
            'fake_name'
        )

        self.fake_driver.resource.create_instances.\
            assert_called_once_with(
                ImageId='fake_image_id',
                MinCount=1,
                MaxCount=1,
                InstanceType='fake_flavor_id',
                SubnetId='fake_net_id',
                IamInstanceProfile={
                    'Arn': '',
                    'Name': 'fake_name'
                }
            )

    def test_create_without_instance_name(self):
        self.mock_object(
            self.fake_driver.resource, 'create_instances',
            mock.Mock(return_value=mock.Mock))

        self.fake_driver.create(
            'fake_image_id',
            'fake_flavor_id',
            'fake_net_id'
        )

        self.fake_driver.resource.create_instances. \
            assert_called_once_with(
                ImageId='fake_image_id',
                MinCount=1,
                MaxCount=1,
                InstanceType='fake_flavor_id',
                SubnetId='fake_net_id',
                IamInstanceProfile={
                    'Arn': '',
                    'Name': mock.ANY
                }
            )

    def test_create_unable_to_create_instance(self):
        self.mock_object(
            self.fake_driver.resource, 'create_instances',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError, self.fake_driver.create,
                'fake_image_id',
                'fake_flavor_id',
                'fake_net_id',
                'fake_name')

        self.fake_driver.resource.create_instances. \
            assert_called_once_with(
                ImageId='fake_image_id',
                MinCount=1,
                MaxCount=1,
                InstanceType='fake_flavor_id',
                SubnetId='fake_net_id',
                IamInstanceProfile={
                    'Arn': '',
                    'Name': mock.ANY
                }
            )

    def test_show_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(return_value=fake_describe_return))

        self.fake_driver.show('fake_id')

        self.fake_driver.client.describe_instances. \
            assert_called_once_with(InstanceIds=['fake_id'])

    def test_show_unable_to_show(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.show, 'fake_id')

        self.fake_driver.client.describe_instances. \
            assert_called_once_with(InstanceIds=['fake_id'])

    def test_list_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(return_value=fake_describe_return))

        self.fake_driver.list()

        self.fake_driver.client.describe_instances. \
            assert_called_once_with()

    def test_list_unable_to_list(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.list)

        self.fake_driver.client.describe_instances. \
            assert_called_once_with()

    def test_delete_successfully(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(return_value=FakeInstance()))

        self.fake_driver.delete('fake_id')

    def test_delete_unable_to_list(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.delete, 'fake_id')

    def test_shutdown_successfully(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(return_value=FakeInstance()))

        self.fake_driver.shutdown('fake_id')

    def test_shutdown_unable_to_list(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.shutdown, 'fake_id')

    def test_start_successfully(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(return_value=FakeInstance()))

        self.fake_driver.start('fake_id')

    def test_start_unable_to_list(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.start, 'fake_id')

    def test_reboot_successfully(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(return_value=FakeInstance()))

        self.fake_driver.reboot('fake_id')

    def test_reboot_unable_to_list(self):
        self.mock_object(
            self.fake_driver.resource, 'Instance',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            ))
        )

        self.assertRaises(ClientError,
                          self.fake_driver.reboot, 'fake_id')

    def test_add_nic_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'attach_network_interface',
            mock.Mock(return_value=mock.Mock))

        self.fake_driver.add_nic('fake_id', 'fake_net_id')

        self.fake_driver.client.attach_network_interface. \
            assert_called_once_with('fake_id', 'fake_net_id', 1)

    def test_add_nic_unable_to_add(self):
        self.mock_object(
            self.fake_driver.client, 'attach_network_interface',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )))

        self.assertRaises(ClientError,
                          self.fake_driver.add_nic, 'fake_id', 'fake_net_id')

        self.fake_driver.client.attach_network_interface. \
            assert_called_once_with('fake_id', 'fake_net_id', 1)

    def test_delete_nic_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'detach_network_interface',
            mock.Mock(return_value=mock.Mock))

        self.fake_driver.delete_nic('fake_id', 'fake_attachment_id')

        self.fake_driver.client.detach_network_interface. \
            assert_called_once_with('fake_attachment_id')

    def test_delete_nic_unable_to_delete(self):
        self.mock_object(
            self.fake_driver.client, 'detach_network_interface',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )))

        self.assertRaises(ClientError,
            self.fake_driver.delete_nic, 'fake_id', 'fake_attachment_id')

        self.fake_driver.client.detach_network_interface. \
            assert_called_once_with('fake_attachment_id')

    def test_list_nic_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(return_value=fake_describe_return))

        self.fake_driver.list_nic('fake_id')

        self.fake_driver.client.describe_instances. \
            assert_called_once_with(InstanceIds=['fake_id'])

    def test_list_nic_unable_to_list(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )))

        self.assertRaises(ClientError,
                          self.fake_driver.list_nic, 'fake_id')

        self.fake_driver.client.describe_instances. \
            assert_called_once_with(InstanceIds=['fake_id'])

    def test_list_ip_successfully(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(return_value=fake_describe_return))

        self.fake_driver.list_ip('fake_id')

        self.fake_driver.client.describe_instances. \
            assert_called_once_with(InstanceIds=['fake_id'])

    def test_list_ip_unable_to_delete(self):
        self.mock_object(
            self.fake_driver.client, 'describe_instances',
            mock.Mock(side_effect=ClientError(
                fake_error_code,
                'operation_name'
            )))

        self.assertRaises(ClientError,
                          self.fake_driver.list_ip, 'fake_id')

        self.fake_driver.client.describe_instances. \
            assert_called_once_with(InstanceIds=['fake_id'])

