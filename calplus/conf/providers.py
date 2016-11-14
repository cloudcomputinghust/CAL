"""Provider Configuration"""
from oslo_config import cfg


provider_group = cfg.OptGroup('providers',
                              title='Supported Providers')

openstack_group = cfg.OptGroup('openstack',
                         title='OpenStack Hosts')

amazon_group = cfg.OptGroup('amazon',
                      title='Amazon Hosts')

driver_mapper = cfg.DictOpt('driver_mapper',
                            default={
                                'openstack': 'OpenstackDriver',
                                'amazon': 'AmazonDriver',
                            },
                            help="""
                            Dict with key is provider, and value is
                            Driver class.
                            """)

# All above configurations is temporary. Will be updated.

# Openstack Authenticate Configuration.

os1_auth_opts = {
    'os_auth_url': 'http://host1:35357/v3',
    'os_project_name': 'admin',
    'os_username': 'admin',
    'os_password': 'ADMIN_PASS',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'os_identity_api_version': '3',
    'os_image_api_version': '2',
    'tenant_id': 'fake_tenant_id',
    'os_novaclient_version': '2.1',
    'limit': {
        "subnet": 10,
        "network": 10,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}

os2_auth_opts = {
    'os_auth_url': 'http://host2:35357/v3',
    'os_project_name': 'admin',
    'os_username': 'admin',
    'os_password': 'ADMIN_PASS',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'os_identity_api_version': '3',
    'os_image_api_version': '2',
    'tenant_id': 'fake_tenant_id',
    'limit': {
        "subnet": 10,
        "network": 10,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}

os_hosts = cfg.DictOpt(
    'hosts',
    default={
        'openstack1': os1_auth_opts,
        'openstack2': os2_auth_opts,
    },
    help='List of available OpenStack Hosts'
)

# Amazon Authenticate Configuration.
aws1_auth_opts = {
    'aws_access_key_id': 'c543fa29eeaf4894a1078ec0860baefd',
    'aws_secret_access_key': 'd2246a2235ca40ffa7fbf817ae1108ba',
    'region_name': 'RegionOne',
    'endpoint_url': 'http://192.168.122.75:8788',
    'limit': {
        "subnet": 10,
        "vpc": 5,
        "floatingip": 50,
        "subnetpool": -1,
        "security_group_rule": 100,
        "security_group": 10,
        "router": 10,
        "rbac_policy": -1,
        "port": 50
    }
}


aws_hosts = cfg.DictOpt(
    'hosts',
    default={
        'aws1': aws1_auth_opts
    },
    help='List of available Amazon Hosts'
)

provider_opts = [
    driver_mapper,
]

openstack_opts = [
    os_hosts,
]

amazon_opts = [
    aws_hosts,
]


def register_opts(conf):
    conf.register_group(provider_group)
    conf.register_opts(provider_opts, group=provider_group)
    conf.register_group(openstack_group)
    conf.register_opts(openstack_opts, group=openstack_group)
    conf.register_group(amazon_group)
    conf.register_opts(amazon_opts, group=amazon_group)


def list_opts():
    return {
        provider_group: provider_opts,
        openstack_group: openstack_opts,
        amazon_group: amazon_opts,
    }
