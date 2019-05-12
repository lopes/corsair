# Corsair > IANA > RDAP
This is the [IANA RDAP](https://data.iana.org/rdap/) API wrapper.


## Basic Usage

```python
>>> from corsair.iana.rdap import Api
>>> rdap = Api()
>>> rdap.asn
for k,v in rdap.asn.items():
    for r in v:
        if asn in r:
            print(k)
```
