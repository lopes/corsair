# Corsair > Cisco > ISE
This is the [Cisco Identity Services Engine (ISE)](https://www.cisco.com/c/en/us/products/security/identity-services-engine/index.html) API wrapper.  First, you must enable the "External Restful Services" in ISE, so the system will be able to be accessed through API.  After that, the whole documentation can be read at `https://ise.corp:9060/ers/sdk`.

Prerequisites:

* Tested under ISE 2.2
* URL for API (usually `https://ise.corp:9060/ers/config`)
* Credentials for API access

It's important to notice that ISE uses certain filters and all are passed by `filter` command.  Since it's not possible to do that in Python, programmers must use `filter1`, `filter2`, ..., `filterN` and they'll be converted accordingly by `Request.process_filters()` method.  See an example below.


## Basic Usage

```python
>>> from corsair.cisco.ise import Api
>>> ise = Api('https://ise.corp:9060/ers/config', 'cors', 'Strong_P4$$w0rd!')
>>> ise.portal.read('18b73f40-5e4e-11e4-b905-005056bf2f0a')
>>> ise.internaluser.read('', filter1='description.CONTAINS.CORS', filter2='name.NSTARTSW.a')
>>> ise.sponsorgroup.read('093b7d92-8f3a-11e7-a879-a0ecf9ce3f08')
```
