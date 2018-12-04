""" OpenstackDriver for Compute
    based on BaseDriver
"""


from datetime import datetime
import six

from keystoneauth1.identity import v3
from keystoneauth1 import session
from cinderclient.v3 import client

from calplus.v1.block_storage.drivers.base  import BaseDriver


PROVIDER = "OPENSTACK"


class CinderDriver(BaseDriver):
    """docstring for OpenstackDriver"""

    def __init__(self, cloud_config):
        super(CinderDriver, self).__init__()
        self.auth_url = cloud_config['os_auth_url']
        self.project_name = cloud_config['os_project_name']
        self.username = cloud_config['os_username']
        self.password = cloud_config['os_password']
        self.user_domain_name = \
            cloud_config.get('os_project_domain_name', 'default')
        self.project_domain_name = \
            cloud_config.get('os_user_domain_name', 'default')
        self.driver_name = \
            cloud_config.get('driver_name', 'default')
        self.tenant_id = cloud_config.get('tenant_id', None)
        self.limit = cloud_config.get('limit', None)
        self.client_version = \
            cloud_config.get('os_cinderclient_version', '4.1.0')
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)
        sess = session.Session(auth=auth)

        self.client = client.Client(self.client_version, session=sess)

    def create(self, configs):
        size = configs.get('size')
        consistencygroup_id = configs.get('consistencygroup_id')
        group_id = configs.get('group_id')
        snapshot_id = configs.get('snapshot_id')
        source_volid = configs.get('source_volid')
        name = configs.get('name')
        description = configs.get('description')
        volume_type = configs.get('volume_type')
        user_id = None,
        project_id = None
        availability_zone = configs.get('availability_zone')
        metadata = configs.get('metadata')
        imageRef = configs.get('imageRef')
        scheduler_hints = configs.get('scheduler_hints')
        multiattach = configs.get('multiattach')
        backup_id = configs.get('backup_id')

        volume = self.client.volumes.create(size, consistencygroup_id,
                        group_id, snapshot_id,
                        source_volid, name, description,
                        volume_type, user_id,
                        project_id, availability_zone,
                        metadata, imageRef, scheduler_hints,
                        multiattach, backup_id)
        return volume

    def list(self):
        return self.client.volumes.list()

    def get(self, volume_id):
        return self.client.volumes.get(volume_id)

    def attach(self, volume, instance_uuid=None):
        mountpoint = '/dev/vda'
        mode = 'rw'
        return self.client.volumes.attach(volume, instance_uuid, mountpoint, mode)

    def set_bootable(self, volume, flag):
        return self.client.volumes.set_bootable(self, volume, flag)