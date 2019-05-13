# Corsair > IANA > RDAP
This is the [IANA RDAP](https://data.iana.org/rdap/) API wrapper.  It implements common routines to retrive data from RDAP servers, such as IP addresses, domains, and ASN information.  Before any operation, it gets basic information from IANA, to determine which RDAP server must be used.

An example on how RDAP structures URLs and how it's mapped in Corsair follows:

```
https://registar.domain/rdap/domain/lacnic.net
\__________________________/\______/\________/
           Base URL         Endpoint Resource
```

At this point, you cannot use the endpoint `entity` because it's not implemented.  Another constraint is that the endpoint `ip` can't search for a network.


## Basic Usage

```python
>>> from corsair.iana.rdap import Api
>>> rdap = Api()
>>> rdap.ip.read('128.201.18.1')
>>> rdap.asn.read('266604')
>>> rdap.domain.read('cemig.com.br')
```
