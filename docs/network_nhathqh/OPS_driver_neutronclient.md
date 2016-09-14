# OPS Driver - NeutronClient

###Network
```
list_network(self):
	networks = neutron.list_networks('filter_attrs_name': ‘value’)
	# list filter_attrs_name sẽ update sau
```
```
show_network(self):
	network = neutron.show_network(network_id) 
```
```
create_network(self):
	# Với int-net (đề xuất dùng arg type = 'internal')
	network = {
		'name': 'mynetwork',
		'description': 'mydescription'
	}
	neutron.create_network({'network': network})

	# Với ext-net (đề xuất dùng arg type = 'external')
	network = {
		'name': 'mynetwork',
		'router:external': 'true',
		'provider:physical_network': 'external',
		'provider:network_type': 'flat'
	}
	neutron.create_network({'network': network})
```
```
update_network(self):
	network = {
		'name': 'newnetwork',
		'description': 'newdescription'
	}
	neutron.update_network(network_id,{'network': network})
```
```
delete_network(self):
	neutron.delete_network(network_id)
```

```
list_network_ip_availabilities(self):
	network_ip_availabilities =neutron. list_network_ip_availabilities()
```
```
show_network_ip_availability(self):
	network_ip_availability = neutron.show_network_ip_availability(network_id)
```
###Subnet
```
list_subnets(self):
	subnets = neutron.list_subnet()
```
```
show_subnet(self):
	subnet = neutron.show_subnet(subnet_id)
```
```
create_subnet(self):
	subnet = {
        	"network_id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
        	"ip_version": 4,
        	"cidr": "10.0.0.1"
	}
	neutron.create_subnet({'subnet'= subnet}
```
```
update_subnet(self):
	subnet = {
        	"network_id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
        	"ip_version": 4,
        	"cidr": "10.0.0.1"
	}
	neutron.update_subnet(subnet_id,{'subnet': subnet})
```
```
delete_subnet(self):
	neutron.delete_subnet(subnet_id)
```
###Router
```
list_routers(self):
	routers = neutron.list_router()
```
```
show_router(self):
	router = neutron.show_router(router_id)
```
```create_router(self,
create_router(self):
	#nếu là ext-router (router gắn với ext-net)
	router = {
		"name": 'myrouter',
		"external_gateway_info": {
         		"network_id": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
      		}
	}
	neutron.create_router({'router': router})
	#nếu là default-router thì ko cần external_gateway_info
```
```
update_router(self):
	router={...}
	neutron.update_router(router_id)
	
```
```
delete_router(self):
	neutron.delete_router(router_id)	
```
```
add_interface_router(self):
	body = {
    		"subnet_id": "a2f1f29d-571b-4533-907f-5803ab96ead1"
		#hoặc
		"port_id":"a2f1f29d-571b-4533-907f-5803ab96ead1"
	}
	neutron.add_interface_router(router_id,body)
```
```
remove_interface_router(self):
	body = {
    		"subnet_id": "a2f1f29d-571b-4533-907f-5803ab96ead1"
		#hoặc
		"port_id":"a2f1f29d-571b-4533-907f-5803ab96ead1"
	}
	neutron.remove_interface_router(router_id,body)
```
```
add_gateway_router(self):
	body= {
         	"external_network": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
	}
	neutron.add_gateway_router(router_id, body)
```
```
remove_gateway_router(self):
	neutron.add_gateway_router(router_id)
```
###Port
###Quota
```
list_quotas(self):
	quotas = neutron.list_quotas()
	#trả về list quota của các tenant
```
```
show_quota(self):
	quota = neutron.show_quota(tenant_id)
```
```
update_quota(self):
	quota = {
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
	neutron.update_quota(tenant_id, {'quotas': quota})
```
```
delete_quota(self):
	neutron.delete_quota(tenant_id)
	#reset quota of a specified tenant to default
```
###FloatingIP
###Firewall
###Security_Group
###VPN

##References
- https://github.com/openstack/python-neutronclient/blob/master/doc/source/usage/library.rst
- http://developer.openstack.org/api-ref/networking/v2-ext/index.html
- https://github.com/openstack/python-neutronclient/blob/master/neutronclient/v2_0/client.py