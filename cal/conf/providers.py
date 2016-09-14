"""Provider Configuration"""
from oslo_config import cfg


provider_group = cfg.OptGroup('providers',
                              title='Supported Providers')

openstack_group = cfg.OptGroup('openstack',
                         title='OpenStack Hosts')

amazon_group = cfg.OptGroup('amazon',
                      title='Amazon Hosts')

opennebula_group = cfg.OptGroup('openebula',
                          title='OpenNebula Hosts')

driver_mapper = cfg.DictOpt('driver_mapper',
                            default={
                                'openstack': 'OpenstackDriver',
                                'amazon': 'AmazonDriver',
                                'opennebula': 'OpennebulaDriver',
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
    'os_image_api_version': '2'
}

os2_auth_opts = {
    'os_auth_url': 'http://host2:35357/v3',
    'os_project_name': 'admin',
    'os_username': 'admin',
    'os_password': 'ADMIN_PASS',
    'os_project_domain_name': 'default',
    'os_user_domain_name': 'default',
    'os_identity_api_version': '3',
    'os_image_api_version': '2'
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

aws1_auth_opts = {}
aws2_auth_opts = {}

aws_hosts = cfg.DictOpt(
    'hosts',
    default={
        'aws1': aws1_auth_opts,
        'aws2': aws2_auth_opts
    },
    help='List of available Amazon Hosts'
)

# OpenNebula Authenticate Configuration.

on1_auth_opts = {}
on2_auth_opts = {}

on_hosts = cfg.DictOpt(
    'hosts',
    default={
        'on1': on1_auth_opts,
        'on2': on2_auth_opts,
    },
    help='List of available OpenNebula Hosts'
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

opennebula_opts = [
    on_hosts,
]


def register_opts(conf):
    conf.register_group(provider_group)
    conf.register_opts(provider_opts, group=provider_group)
    conf.register_group(openstack_group)
    conf.register_opts(openstack_opts, group=openstack_group)
    conf.register_group(amazon_group)
    conf.register_opts(amazon_opts, group=amazon_group)
    conf.register_group(opennebula_group)
    conf.register_opts(opennebula_opts, group=opennebula_group)


def list_opts():
    return {
        provider_group: provider_opts,
        openstack_group: openstack_opts,
        amazon_group: amazon_opts,
        opennebula_group: opennebula_opts
    }
