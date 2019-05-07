# Corsair > Digital Ocean > NetBox
This is the [Digital Ocean NetBox](https://github.com/digitalocean/netbox) API wrapper.  It's based on [pynetbox](https://github.com/digitalocean/pynetbox), Digital Ocean's official API client library for NetBox.  API is well documented NetBox is self-explanatory and is available at `https://netbox.corp/api/docs`.

Prerequisites:

* NetBox 2.4.4 (the environment I had to test)
* Access credentials (token)

```
https://netbox.corp/api/ipam/ip-addresses/360/
\_____________________/\____/\______________/\_/
      Base URL        Endpoint   Resource    Suffix
```


## Basic Usage

```python
>>> from corsair.digitalocean.netbox import Api
>>> netbox = Api('https://netbox.corp/api', 'aR3allyl000ngtok3n')
>>>
>>> ip = netbox.ipam.create('ip-addresses', address='10.0.1.2', description='Corsair')
>>> netbox.ipam.read('ip-addresses', address='10.0.1.2')
>>> netbox.ipam.read(f'ip-addresses/{ip["id"]}')
>>> netbox.ipam.update(f'ip-addresses/{ip["id"]}', description='foobar')
>>> netbox.ipam.delete(f'ip-addresses/{ip["id"]}')
>>> all_ips = netbox.ipam.read('ip-addresses')
```
