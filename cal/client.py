from cal import exceptions
from cal.v1.compute import client as compute_client_v1
from cal.v1.network import client as network_client_v1
from cal.v1.storage import client as storage_client_v1
from cal.version import __version__

_CLIENTS = {
    '1.0.0': {
        'compute': compute_client_v1.Client,
        'network': network_client_v1.Client,
        'storge': storage_client_v1.Client,
    }
}


def Client(url=None, version=__version__,
           resource=None, provider=None, **kwargs):
    """Initialize client object based on given version.

    :params url:
    :params version: version of CAL, define at setup.cfg
    :params resource: resource type
    :params provider: cloud provider(Openstack, Amazon...)
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
    try:
        return _CLIENTS[version][resource](url, provider, **kwargs)
    except KeyError:
        raise exceptions.UnsupportedVersion(
                                'Unknown client version or subject')
