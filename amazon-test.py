
import time
from calplus.v1.compute.drivers.amazon import AmazonDriver
from calplus.v1.block_storage.drivers.amazon import AmazonVolumeDriver
from calplus.v1.network.drivers.amazon import AmazonNetDriver
import argparse

amazon_config_driver = {
    'driver_name': 'AMAZON1',
    'aws_access_key_id': '9d0e9902b3984d22a179b28df675ad80',
    'aws_secret_access_key': '8404f669a8a74195a15ad46171a3b548',
    'region_name': 'RegionOne',
    'endpoint_url': 'http://controller:8788',
    'limit': {
    }
}

class AmazonTest():
    def __init__(self):
        self.amazon_driver = AmazonDriver(amazon_config_driver)
        self.amazon_volume_driver = AmazonVolumeDriver(amazon_config_driver)
        self.amazon_net_driver = AmazonNetDriver(amazon_config_driver)

    def create_vm_small_flavor(self, block_device_mapping=None):
        started_time = int(round(time.time() * 1000))
        image_id = 'ami-9e6af129'
        # if block_device_mapping is not None:
        #     image_id = 'ami-9e6af129'
        self.amazon_driver = AmazonDriver(amazon_config_driver)
        result = self.amazon_driver.create(
            'm1.small',
            'subnet-94e5201d',
            'cal',  # keypair
            block_device_mapping,
            image_id,
        )
        print (result[0])
        if(result[0]):
            ended_time = int(round(time.time() * 1000))
            print 'SMALL_FLAVOR CREATED_TIME (ms): ', ended_time - started_time
            # self.delete_server(result[0].id)
        return result[0]

    def create_vm_medium_flavor(self, block_device_mapping=None):
        started_time = int(round(time.time() * 1000))
        image_id = 'ami-9e6af129'
        # if block_device_mapping is not None:
        #     image_id = None
        self.amazon_driver = AmazonDriver(amazon_config_driver)
        result = self.amazon_driver.create(
            block_device_mapping,
            image_id,
            'm1.medium',
            'subnet-94e5201d',
            'cal'  # keypair
        )
        print (result[0])
        if(result[0]):
            ended_time = int(round(time.time() * 1000))
            print 'MEDIUM_FLAVOR CREATED_TIME (ms): ', ended_time - started_time
            # self.delete_server(result[0].id)
        return result[0]

    def create_vm_large_flavor(self, block_device_mapping=None):
        started_time = int(round(time.time() * 1000))
        image_id = 'ami-9e6af129'
        # if block_device_mapping is not None:
        #     image_id = None
        self.amazon_driver = AmazonDriver(amazon_config_driver)
        result = self.amazon_driver.create(
            block_device_mapping,
            image_id,
            'm1.large',
            'subnet-94e5201d',
            'cal'  # keypair
        )
        print (result[0])
        if(result[0]):
            ended_time = int(round(time.time() * 1000))
            print 'LARGE_FLAVOR CREATED_TIME (ms): ', ended_time - started_time
            # self.delete_server(result[0].id)
        return result[0]

    def delete_server(self, id):
        time.sleep(10)
        print 'DELETED', id
        self.amazon_driver.delete(id)
        time.sleep(10)

    def create_volume(self):
        configs = {
            'size': 15,
            'name': 'Amazon-Cal-Vol-Test',
            'snapshot_id': 'snap-e6bfaec3'
        }
        return self.amazon_volume_driver.create(configs)

    def create_snapshot(self):
        configs = {
            'description': 'snapshot for testing CAL with EC2',
            'name': 'cal-snapshot'
        }
        return self.amazon_volume_driver.create_snapshot(configs)

    def associate_public_ip(self, allocation_id, instance_id):
        started_time = int(round(time.time() * 1000))
        configs = {
            'allocation_id': allocation_id,
            'instance_id': instance_id
        }
        result = self.amazon_driver.associate_public_ip(configs)
        ended_time = int(round(time.time() * 1000))
        print 'Associate Public IP in (ms): ', ended_time - started_time
        return result

    def is_valid_pub_ip(self, pub_ip):
        search_opts = {
            'Filters': [
                {
                    'Name': 'network-interface.addresses.association.public-ip',
                    'Values': [
                        pub_ip,
                    ]
                },
            ]
        }
        instances = self.amazon_driver.list(**search_opts)
        return False if len(instances) else True

def processArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--flavor', dest='FLAVOR', type=str, default="")
    parser.add_argument('--volume', dest='VOLUME', type=str, default="false")
    parser.add_argument('--size', dest='SIZE', type=str, default="20")
    parser.add_argument('--assign-ip', dest='ASSIGN', type=str, default="false")
    args = parser.parse_args()
    return args


def run():

    args = processArguments()
    amazon_test = AmazonTest()
    if args.FLAVOR == 'small':
        print 'small type vm'
        amazon_test.create_vm_small_flavor()
    elif args.FLAVOR == 'medium':
        print 'medium type vm'
        amazon_test.create_vm_medium_flavor()
    elif args.FLAVOR == 'large':
        print 'large type vm'
        amazon_test.create_vm_large_flavor()

    if args.VOLUME == 'true':
        started_time = int(round(time.time() * 1000))
        print 'create volume'
        # volume = amazon_test.create_volume()

        print 'create instance'
        block_device_mapping = [
            {
                'DeviceName': '/dev/vdb',
                'VirtualName': 'ephemeral0',
                'Ebs': {
                    'DeleteOnTermination': False,
                    'SnapshotId': 'snap-e6bfaec3',
                    'VolumeSize': int(args.SIZE),
                    'VolumeType': '',
                    'Encrypted': False,
                    'KmsKeyId': ''
                },
                'NoDevice': ''
            },
        ]
        vm = amazon_test.create_vm_small_flavor(block_device_mapping)

        ended_time = int(round(time.time() * 1000))
        print 'CREATE VOLUME WITH SIZE ' + args.SIZE + 'GB IN (ms): ', ended_time - started_time

        f = open('amazon_saved_vm.txt', 'w+')
        f.write(str(vm.id))  # write to file

    if args.ASSIGN != 'false':
        print 'Associate Floating IP'
        f = open("amazon_saved_vm.txt", "rw+")
        vm_id = f.readline()
        print vm_id
        search_opts = {
            'Filters': [
                {
                    'Name': 'domain',
                    'Values': [
                        'vpc',
                    ]
                }
            ]
        }
        ips = amazon_test.amazon_net_driver.list_public_ip(**search_opts)
        has_pub_ip = False
        for ip in ips:
            is_valid = amazon_test.is_valid_pub_ip(ip['public_ip'])
            if is_valid:
                has_pub_ip = True
                amazon_test.associate_public_ip(ip['id'], vm_id)
                break

        if has_pub_ip == False:
            print "Has no public IP"

    # else:
    #     print 'all type vm'
    #     amazon_test.create_vm_small_flavor()
    #     time.sleep(3)
    #     amazon_test.create_vm_medium_flavor()
    #     time.sleep(3)
    #     amazon_test.create_vm_large_flavor()



if __name__ == "__main__":
    run()