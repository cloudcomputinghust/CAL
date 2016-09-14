import logging

import cal.conf
from cal import exceptions
from cal import utils
from cal.v1.compute import client as compute_client_v1
from cal.v1.network import client as network_client_v1
from cal.v1.block_storage import client as block_storage_client_v1
from cal.v1.object_storage import client as object_storage_client_v1
from cal.version import __version__

LOG = logging.getLogger(__name__)

CONF = cal.conf.CONF

_CLIENTS = {
    '1.0.0': {
        'compute': compute_client_v1.Client,
        'network': network_client_v1.Client,
        'block_storage': block_storage_client_v1.Client,
        'object_storge': object_storage_client_v1.Client,
    }
}


def Client(version=__version__, resource=None,
           provider=None, cloud_config=None, **kwargs):
    """Initialize client object based on given version.

    :params version: version of CAL, define at setup.cfg
    :params resource: resource type
                     (network, compute, object_storage, block_storage)
    :params provider: cloud provider(Openstack, Amazon...)
    :params cloud_config: cloud auth config
    :params **kwargs: specific args for resource
    :return: class Client

    HOW-TO:
    The simplest way to create a client instance is initialization::

        >> from cal import client
        >> cal = client.Client(version='1.0.0',
                               resource='compute',
                               provider='OpenStack',
                               some_needed_args_for_ComputeClient)
    """

    versions = _CLIENTS.keys()

    if version not in versions:
        raise exceptions.UnsupportedVersion(
            'Unknown client version or subject'
        )

    resources = _CLIENTS[version].keys()
    providers = CONF.providers.driver_mapper.keys()

    if provider is None:
        provider = utils.pick_cloud_provider()

    elif provider.lower() not in providers:
        raise exceptions.ProviderNotFound(
            'Unknow provider.'
        )

    if resource is None:
        raise exceptions.ResourceNotDefined(
            'Not define Resource, choose one: compute, network,\
            object_storage, block_storage.'
        )

    elif resource.lower() not in resources:
        raise exceptions.ResourceNotFound(
            'Unknow resource: compute, network,\
                        object_storage, block_storage.'
        )

    _cloud_config = utils.pick_host_with_specific_provider(provider,
                                                           cloud_config)

    LOG.info('Instantiating {} client ({})' . format(resource, version))

    return _CLIENTS[version][resource](provider, _cloud_config, **kwargs)
