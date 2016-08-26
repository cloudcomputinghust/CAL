# Cloud Network Quota Survey

| Openstack | AWS EC2 | Abstract Quota|
|---|---|---|
| network, subnet | vpc (per region), subnet (per vpc) | Network |
| port |  |  |
| router | route tables (per VPC) | Router |
| Security groups |  Security groups (per VPC) | Security groups |
| Security group rules | Security group rules | Security group rules |
| Floating IP | Elastic IP | Floating IP |
| | internet gateway per region | Internet gateway |
| VPN services, IPSec | VPN gateway | VPN gateway |
|   | Network interface (per VM) |   |
|   | VPC endpoints per region |   |
| FaaS | Network ACLs (per VPC) | Firewall |
| Firewall rules | Network ACL rules | Firewall rules |

# Abstract Network Quota Proposal

####Commitment:
OPS: 
- 1 network only have 1 subnet
EC2:
- 

...

#### Example of Quota (Dict Format)

```
network_quota:
{
	"networks":
	{
		"max": 50,
		"used": 5,
		"list_cidrs": [
					{"net_id": net01, "cidr": 10.0.0.0/24}, 
					{"net_id": net01, "cidr": 10.0.1.0/24}, 
					{"net_id": net01, "cidr": 10.10.0.0/16}, 
					{"net_id": net01, "cidr": 10.20.0.0/16}, 
					{"net_id": net01, "cidr": 10.0.2.192/28}
				]
		"VPCs": //  = none với Cloud là OPS
		{
			"max": 5,
			"used":1,
			"list_cidrs": [{"vpc_id":vpc01, "cidr": 10.0.0.0/8}]
		}
	},
	"security_groups":
	{
		"max": 50,
		"used": 1,
		"list_security_groups": [
						{
							"security_group_id":secgroup01,		
							"rules_max":50},
							"rules_used":10,
							"list_rules":[...]
						}
					]
	},
	"floating_ip":
	{
		"max":10,
		"used":5,
		"list_floating_ips":[...]
	},
	"router":
	{
		"max":50,
		"used":1,
		"list_routers":[
					{
						"router_id":router01, 
						"is_gateway":false
					} 
				]
	// is_gateway = true if router connect to external-net of OPS
	},
	"internet_gateway":
	{
		"max":5,
		"used":1,
		"list_internet_gateways": [{"internet_gateway_id":igw01}]
	},
	"vpn_gateway":
	{
		"max":5,
		"used":1,
		"list_vpn_gateways":[
							{
								"vpn_gateway_id":vnp01,
								"max_connections":10,
								"used_connections":1,
								"list_connections":[...]
							}
						]
	}
	"firewall"::
	{
		"max": 50,
		"used": 1,
		"list_firewalls": [
						{
							"firewall_id":fw01,		
							"rules_max":50},
							"rules_used":10,
							"list_rules":[...]
						}
					]
	},
}
```

##References
- http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Appendix_Limits.html
- http://docs.openstack.org/mitaka/config-reference/networking/networking_options_reference.html#quotas
