# Corsair > IANA > RDAP
This is the [IANA RDAP](https://data.iana.org/rdap/) API wrapper.


## Basic Usage

```python
>>> import ipaddress
>>> from corsair.iana.rdap import Api
>>>
>>> rdap = Api()
>>> asn = 266604
>>> ipv4 = ipaddress.ip_address('128.201.18.1')
>>> ipv6 = ipaddress.ip_address('2801:80:1ce0::')
>>>
>>> for k,v in rdap.asn.items():
...     for r in v:
...         if asn in r:
...             print(k)
>>> for k,v in rdap.ipv4.items():
...     for net in v:
...         if ipv4 in net:
...             print(k)
>>> for k,v in rdap.ipv6.items():
...     for net in v:
...         if ipv6 in net:
...             print(k)
```
