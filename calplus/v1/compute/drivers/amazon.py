""" OpenstackDriver for Compute
    based on BaseDriver
"""


from datetime import datetime
import six

import boto3

from calplus.v1.compute.drivers.base import BaseDriver, BaseQuota


PROVIDER = "AMAZON"


class AmazonDriver(BaseDriver):
    """docstring for AmazonDriver"""

    def __init__(self, cloud_config):
        super(AmazonDriver, self).__init__()
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
        self.quota = AmazonQuota(self.client, self.limit)

    def create(self, flavor_id,
               network_id, key_name, block_device_mapping=None, image_id=None, name=None, number=1, **kargs):
        if name is None:
            name = six.text_type(datetime.now())
        profile = {
            'Arn': '',
            'Name': name
        }
        server = self.resource.create_instances(
            BlockDeviceMappings=block_device_mapping,
            ImageId=image_id,
            MinCount=number,
            MaxCount=number,
            KeyName=key_name,
            InstanceType=flavor_id,
            SubnetId=network_id,
            IamInstanceProfile=profile
        )
        return server

    def create_key_pair(self, key_name=''):
        return self.client.create_key_pair(
            KeyName=key_name
        )

    def show(self, instance_id):
        servers = self.client.describe_instances(InstanceIds=[instance_id])
        return servers.get("Reservations")[0].get("Instances")[0]

    def list(self, **search_opts):
        # TODO: reformat search_opts for client boto
        servers = self.client.describe_instances(**search_opts)
        if len(servers.get("Reservations")):
            return servers.get("Reservations")[0].get("Instances")
        return []

    def delete(self, instance_id):
        server = self.resource.Instance(instance_id)
        return server.terminate()

    def shutdown(self, instance_id):
        server = self.resource.Instance(instance_id)
        return server.stop()

    def start(self, instance_id):
        server = self.resource.Instance(instance_id)
        return server.start()

    def reboot(self, instance_id):
        server = self.resource.Instance(instance_id)
        return server.reboot()

    def resize(self, instance_id, configuration):
        pass

    def add_sg(self, instance_id, new_sg):
        """Add a security group"""
        pass

    def delete_sg(self, instance_id, new_sg):
        """Delete a security group"""
        pass

    def list_sg(self, instance_id):
        """List all security group"""
        pass

    def add_nic(self, instance_id, net_id):
        """Add a Network Interface Controller"""
        return self.client.attach_network_interface(
            instance_id, net_id, 1)

    def delete_nic(self, instance_id, AttachmentId):
        """Delete a Network Interface Controller"""
        return self.client.detach_network_interface(AttachmentId)

    def list_nic(self, instance_id):
        """List all Network Interface Controller"""
        output = self.client.describe_instances(InstanceIds=[instance_id])
        output = output.get("Reservations")[0].get("Instances")[0]
        return output.get("NetworkInterfaces")

    def add_private_ip(self):
        """Add private IP"""
        pass

    def delete_private_ip(self):
        """Delete private IP"""
        pass

    def associate_public_ip(self, configs):
        """Associate a external IP"""
        allocation_id = configs['allocation_id']
        instance_id = configs['instance_id']
        response = self.client.associate_address(
            AllocationId=allocation_id,
            InstanceId=instance_id,
            AllowReassociation=True
        )
        return response

    def disassociate_public_ip(self, public_ip_id):
        """Disassociate a external IP"""
        pass

    def list_ip(self, instance_id):
        """Add all IPs"""
        output = self.client.describe_instances(InstanceIds=[instance_id])
        output = output.get("Reservations")[0].get("Instances")[0]
        ips = {}
        ips['PrivateIp'] = output.get("PrivateIpAddress")
        ips['PublicIp'] = output.get("PublicIpAddress")
        return ips


class AmazonQuota(BaseQuota):

    """docstring for AmazonQuota"""

    def __init__(self, client, limit=None):
        super(AmazonQuota, self).__init__()
        self.client = client
        self.limit = limit
        self._setup()

    def _setup(self):
        pass
