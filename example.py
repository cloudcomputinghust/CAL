"""
Cloud Abstract Layer (CAL) Library Examples
This script shows the basic use of the CAL as a library.
"""
import logging

from cal import client

LOG = logging.getLogger('')

_VERSION = '1.0.0'
_RESOURCES = ['network', 'compute']
_PROVIDER = 'OpenStack'


def run():
    """Run the examples"""

    # NOTE(kiennt): Until now, this example isn't finished yet,
    #               because we don't have any completed driver

    # Get a network client with openstack driver.

    network_client = client.Client(version=_VERSION,
                        resource=_RESOURCES[0], provider=_PROVIDER)
    # net = network_client.create('daikk', '10.0.0.0/24')
    # list_subnet = network_client.list()
    # network_client.show(list_subnet[0].get("id"))
    network_client.delete("4b983028-0f8c-4b63-b10c-6e8420bb7903")

    # Get a compute client with openstack driver.

    # compute_client = client.Client(version=_VERSION,
    #                                resource=_RESOURCES[1],
    #                                provider=_PROVIDER)

    # Create VM.
    # new_vm = compute_client.create_vm(*args, **kwargs)
    # List all VM.
    # vms = compute_client.list_vm(*args, **kwargs)
    # TODO(kiennt): Print ids.
    # Show usage resource.


if __name__ == "__main__":
    run()
