""" OpenstackDriver for Compute
    based on BaseDriver
"""



import six
import boto3

from calplus.v1.block_storage.drivers.base import BaseDriver


PROVIDER = "OPENSTACK"


class AmazonVolumeDriver(BaseDriver):
    """docstring for OpenstackDriver"""

    def __init__(self, cloud_config):
        super(AmazonVolumeDriver, self).__init__()
        self.aws_access_key_id = cloud_config['aws_access_key_id']
        self.aws_secret_access_key = cloud_config['aws_secret_access_key']
        self.endpoint_url = cloud_config['endpoint_url']
        self.region_name = cloud_config.get('region_name', None)
        self.driver_name = \
            cloud_config.get('driver_name', 'default')
        self.limit = cloud_config.get('limit', None)
        self._setup()

    def _setup(self):
        parameters = {
            'aws_access_key_id': self.aws_access_key_id,
            'aws_secret_access_key': self.aws_secret_access_key,
            'region_name': self.region_name,
            'endpoint_url': self.endpoint_url
        }
        self.resource = boto3.resource('ec2', **parameters)
        self.client = boto3.client('ec2', **parameters)

    def create(self, configs):
        avail_zone = "nova"
        snapshot_id = configs.get('snapshot_id')

        # size = configs.get('size')
        # volume_type = 'standard'
        # kms_key_id = ''
        # name = configs.get('name')
        # tags = [{
        #     'ResourceType': 'volume',
        #     'Tags': [
        #         {
        #             'Key': 'name',
        #             'Value': name
        #         },
        #     ]
        # }]

        volume = self.resource.create_volume(
            AvailabilityZones=avail_zone,
            SnapshotId=snapshot_id,
        )
        return volume

    def create_snapshot(self, configs):
        des = configs['description']
        name = configs['name']
        tags = [{
            'ResourceType': 'snapshot',
            'Tags': [
                {
                    'Key': 'name',
                    'Value': name
                },
            ]
        }]
        snapshot = self.resource.create_snapshot(
            Description=des,
            TagSpecifications=tags
        )
        return snapshot

