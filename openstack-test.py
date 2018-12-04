"""
Cloud Abstract Layer (CAL) Library Examples
This script shows the basic use of the CAL as a library.
"""

import time
import pickle
import argparse
from calplus.v1.compute.drivers.openstack import OpenstackDriver
from calplus.v1.block_storage.drivers.openstack import CinderDriver
from calplus.v1.network.drivers.openstack import NeutronDriver

openstack_config_driver = {
    'os_auth_url': 'http://controller:5000/v3',
    'os_username': 'nghiadt',
    'os_password': 'bkcloud',
    'os_project_name': 'nghiadt',
    '': 'http://controller:9696',
    'os_driver_name': 'default',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'tenant_id': '364928bae40f4d55ac6d9b35e2146dc9',
    'limit': {
    }
}

class OpenstackTest():
    def __init__(self, args):
        self.openstack_driver = OpenstackDriver(openstack_config_driver)
        self.cinder_driver = CinderDriver(openstack_config_driver)
        self.neutron_driver = NeutronDriver(openstack_config_driver)
        # if args.FLAVOR:
        #
        # if args.VOLUME == 'true':

    def create_vm_small_flavor(self, block_id=None):
        started_time = int(round(time.time() * 1000))
        image_id = '12162d01-2eab-45db-a1c4-831725aa05ee'
        if block_id is not None:
            image_id = None

        result = self.openstack_driver.create(
            'fd842c76-42bd-41d4-8917-02390eabac9d',  # flavor id
            '60b89cd1-0a5b-4293-bcbe-49be0cc85435',
            '9thfloor-hlf',
            image_id,
            'ops-small-flavor',
            block_id
        )
        print (result)
        if result:
            ended_time = int(round(time.time() * 1000))
            print 'SMALL_FLAVOR CREATED_TIME (ms): ', ended_time - started_time
            # self.delete_server(result)

        return result

    def create_vm_medium_flavor(self, block_id=None):
        started_time = int(round(time.time() * 1000))
        image_id = '12162d01-2eab-45db-a1c4-831725aa05ee'
        if block_id is not None:
            image_id = None
        result = self.openstack_driver.create(
            'd6cff5fd-3083-4b55-972d-46f9aecf973c', # flavor id
            '60b89cd1-0a5b-4293-bcbe-49be0cc85435',
            '9thfloor-hlf',
            image_id,
            'ops-medium-flavor',
            block_id
        )
        print (result)
        if result:
            ended_time = int(round(time.time() * 1000))
            print 'MEDIUM_FLAVOR CREATED_TIME (ms): ', ended_time - started_time
            # self.delete_server(result)

        return result

    def create_vm_large_flavor(self, block_id=None):
        started_time = int(round(time.time() * 1000))
        image_id = '12162d01-2eab-45db-a1c4-831725aa05ee'
        if block_id is not None:
            image_id = None
        result = self.openstack_driver.create(
            '81fdfda4-be44-46f7-9c8f-b15fa1c7ac82', # flavor id
            '60b89cd1-0a5b-4293-bcbe-49be0cc85435',
            '9thfloor-hlf',
            image_id,
            'ops-large-flavor',
            block_id
        )
        print (result)
        if result:
            ended_time = int(round(time.time() * 1000))
            print 'LARGE_FLAVOR CREATED_TIME (ms): ', ended_time - started_time
            # self.delete_server(result)

        return result

    def show_server(self, id):
        server = self.openstack_driver.show(id)
        print server

    def delete_server(self, id):
        time.sleep(10)
        print 'DELETED', id
        self.openstack_driver.delete(id)
        time.sleep(10)

    def list_nic(self, id):
        interfaces = self.openstack_driver.list_nic(id)
        print interfaces

    def create_volume(self, size):
        configs = {}
        configs['size'] = size
        configs['snapshot_id'] = None
        configs['name'] = 'ubuntu-volume-cal'
        configs['description'] = 'cal-test-vol'
        configs['availability_zone'] = 'nova'
        configs['imageRef'] = '12162d01-2eab-45db-a1c4-831725aa05ee'

        result = self.cinder_driver.create(configs)
        return result

    def associate_public_ip(self, instance_id, public_ip_id, private_ip=None):
        started_time = int(round(time.time() * 1000))
        result = self.openstack_driver.associate_public_ip(instance_id, public_ip_id, private_ip)
        ended_time = int(round(time.time() * 1000))
        print 'Associate Public IP in (ms): ', ended_time - started_time
        return result

def processArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--flavor', dest='FLAVOR', type=str, default="")
    parser.add_argument('--volume', dest='VOLUME', type=str, default="false")
    parser.add_argument('--size', dest='SIZE', type=str, default="20")
    parser.add_argument('--assign-ip', dest='ASSIGN', type=str, default="false")
    args = parser.parse_args()
    return args

def run():
    # python openstack-test.py --flavor small

    args = processArguments()
    openstack_test = OpenstackTest(args)

    if args.FLAVOR == 'small':
        print 'small type vm'
        openstack_test.create_vm_small_flavor()
    elif args.FLAVOR == 'medium':
        print 'medium type vm'
        openstack_test.create_vm_medium_flavor()
    elif args.FLAVOR == 'large':
        print 'large type vm'
        openstack_test.create_vm_large_flavor()

    if args.VOLUME == 'true':
        started_time = int(round(time.time() * 1000))
        print 'create volume'
        volume = openstack_test.create_volume(args.SIZE)

        print 'create VM'
        volume_dict = [{
            'boot_index': 0,
            'uuid': volume.id,
            'device_name': 'vda',
            'source_type': "volume",
            'destination_type': "volume",
            'volume_size': args.SIZE,
            'delete_on_termination': False
        }]
        passCreated = False
        while passCreated == False:
            try:
                vm = openstack_test.create_vm_small_flavor(volume_dict)
                print vm, type(vm)
                passCreated = True
            except:
                print 'Volume has been not bootable.'
                time.sleep(3)
        ended_time = int(round(time.time() * 1000))
        print 'CREATE VOLUME WITH SIZE ' + args.SIZE + 'GB IN (ms): ', ended_time - started_time

        f = open('saved_vm.txt', 'w+')
        f.write(str(vm.id)) # write to file

    if args.ASSIGN != 'false':
        print 'Associate Floating IP'
        f = open("saved_vm.txt", "rw+")
        vm_id = f.readline()
        print vm_id
        public_id = args.ASSIGN
        if args.ASSIGN == 'true':
            search_opts = {
                'status': 'DOWN',
                'tenant_id': openstack_config_driver['tenant_id'],
                'description': 'for CAL'
            }
            ips = openstack_test.neutron_driver.list_public_ip(**search_opts)
            public_id = ips[0]['id']
        print openstack_test.associate_public_ip(vm_id, public_id)



    # else:
    #     print 'all type vm'
        # openstack_test.create_vm_small_flavor()
        # time.sleep(3)
        # openstack_test.create_vm_medium_flavor()
        # time.sleep(3)
        # openstack_test.create_vm_large_flavor()


if __name__ == "__main__":
    run()
