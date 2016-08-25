# Network driver documentation

<h3> NetworkDriver Class</h3>
- Attribute : 
  + provider (String) : The name of public provider
  + network_quota : caching network quota in NetworkQuota Class

- Function:
  + create():
  + show():
  + list():
  + update():
  + delete():

<h3> NetworkQuota Class</h3>
- Attribute:
  + networks
  + security_groups
  + floating_ips
  + routers
  + internet_gateways
  + vpn_gateways
  + firewall

- Function:
  + set() : set value for a special quota attribute
  + get() : update network quota from provider. It makes NetworkQuota Class easy to extend network quota attribute.
