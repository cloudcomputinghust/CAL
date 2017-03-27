import logging

import calplus.conf
from calplus import exceptions
from calplus.v1.compute import client as compute_client_v1
from calplus.v1.network import client as network_client_v1
from calplus.v1.block_storage import client as block_storage_client_v1
from calplus.v1.object_storage import client as object_storage_client_v1
from calplus.version import __version__

LOG = logging.getLogger(__name__)

CONF = calplus.conf.CONF

_CLIENTS = {
    '1.0.0': {
        'compute': compute_client_v1.Client,
        'network': network_client_v1.Client,
        'block_storage': block_storage_client_v1.Client,
        'object_storage': object_storage_client_v1.Client,
    }
}


def Client(version=__version__, resource=None, provider=None, **kwargs):
    """Initialize client object based on given version.

    :params version: version of CAL, define at setup.cfg
    :params resource: resource type
                     (network, compute, object_storage, block_storage)
    :params provider: provider object
    :params cloud_config: cloud auth config
    :params **kwargs: specific args for resource
    :return: class Client

    HOW-TO:
    The simplest way to create a client instance is initialization::

        >> from calplus import client
        >> calplus = client.Client(version='1.0.0',
                               resource='compute',
                               provider=provider_object,
                               some_needed_args_for_ComputeClient)
    """

    versions = _CLIENTS.keys()

    if version not in versions:
        raise exceptions.UnsupportedVersion(
            'Unknown client version or subject'
        )

    if provider is None:
        raise exceptions.ProviderNotDefined(
            'Not define Provider for Client'
        )

    support_types = CONF.providers.driver_mapper.keys()

    if provider.type not in support_types:
        raise exceptions.ProviderTypeNotFound(
            'Unknow provider.'
        )

    resources = _CLIENTS[version].keys()

    if not resource:
        raise exceptions.ResourceNotDefined(
            'Not define Resource, choose one: compute, network,\
            object_storage, block_storage.'
        )

    elif resource.lower() not in resources:
        raise exceptions.ResourceNotFound(
            'Unknow resource: compute, network,\
                        object_storage, block_storage.'
        )

    LOG.info('Instantiating {} client ({})' . format(resource, version))

    return _CLIENTS[version][resource](
        provider.type, provider.config, **kwargs)
