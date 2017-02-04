import boto3

from calplus.v1.object_storage.drivers.base import BaseDriver, BaseQuota


PROVIDER = 'AMAZON'


class AmazonDriver(BaseDriver):
    """AmazonDriver for Object Storage"""

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

        self.client = boto3.client('s3', **parameters)
        self.quota = AmazonQuota(self.client, self.limit)

    def create_container(self, container, **kwargs):
        return self.client.create_bucket(Bucket=container, **kwargs)

    def delete_container(self, container):
        return self.client.delete_bucket(Bucket=container)

    def list_containers(self):
        return self.client.list_buckets()

    def stat_container(self, container):
        return self.client.head_bucket(Bucket=container)

    def update_container(self, container, headers, **kwargs):
        pass

    def upload_object(self, container, obj, contents,
                      content_length=None, **kwargs):
        return self.client.put_object(Bucket=container, Key=obj,
                                      ContentLength=content_length,
                                      Body=contents)

    def download_object(self, container, obj, **kwargs):
        return self.client.get_object(Bucket=container, Key=obj)

    def stat_object(self, container, obj):
        return self.client.head_object(Bucket=container, Key=obj)

    def delete_object(self, container, obj, **kwargs):
        return self.client.delete_object(Bucket=container, Key=obj,
                                         **kwargs)

    def list_container_objects(self, container):
        return self.client.list_objects(Bucket=container)

    def update_object(self, container, obj, headers, **kwargs):
        pass

    def copy_object(self, container, obj, destination=None, **kwargs):
        copysource = {
            'Bucket': container,
            'Key': obj
        }

        return self.client.copy_object(Bucket=container, Key=destination,
                                       CopySource=copysource)


class AmazonQuota(BaseQuota):
    """AmazonQuota for ObjectStorage"""

    def __init__(self, client, limit=None):
        super(AmazonQuota, self).__init__()
        self.client = client
        self.limit = limit
        self._setup()

    def _setup(self):
        pass
