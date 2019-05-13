# Corsair
Python wrapper for some NSOC tools.  Corsair aims to implement [RESTFul](https://en.wikipedia.org/wiki/Representational_state_transfer) wrappers for different tools commonly used by Network and Security Operations Centers (NSOC).

The main idea behind Corsair is to provide a method to access different APIs to facilitate the task of integrating tools.  So far, each tool has at least three kinds of classes:

* `Api`: the higher level of abstraction, which connects to the API.
* `Endpoint`: uses endpoints to connect to certain API resources, by using [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) methods.
* `Request`: execute actions in a given API endpoint or resource, using [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).

Each `Api` class has particular properties according to the API it's representing.  The `Endpoint` class implements the CRUD methods themselves, usually:

* `create` to insert new items,
* `read` to retrieve a certain number of items,
* `update` to alter certain items, and
* `delete` to erase items.

The `Request` class implements methods to interact with the server using HTTP, by handling URLs (filter parameters), headers (like `Content-Type` and `Authorization`), and methods (like `GET`, `PUT`, `PATCH`, and `DELETE`).  As all examples accross this repository present, the user will only have to connect to certain API using `Api` classes and understand what endpoints are available in `Endpoint` class.  This should be enough to make all interactions.

## Architecture
It's a project decision to return almost "raw" data from API, so the consumer must treat this data.  This is done because at this point of the project, it'll take a lot of time to understand all resources provided by each API and organize the way they will output data.

This is the URL template Corsair tries to implement:

```
https://app.corp/api/endpoint/resource/suffix?filter=f1&filter2=2
\__________________/\_______/\_______/\_____/\__________________/
     Base URL       Endpoint  Resource Suffix      Filters
\___________________________/\__________________________________/
    Corsair will implement         Corsair will facilitate,
                                 but programmer must implement
```

According to common bibliography, that `suffix` field doesn't exist, but some APIs use it, like IBM/QRadar.  In that case, when the programmer wants details on certain resources, he must insert `/results` in the URL.  It exposes some issues around standardization accross multiple vendors, because some of them wisely prefer to use filters for such things, but others use the `resources` field or even HTTP headers.

By default, Corsair wrappers will verify TLS certificates, but sometimes programmer could want to avoid this behaviour.  That's why `Api` classes have the `tls_verify` parameter set to `True`.  Changing the value to `False` makes Corsair inform to `urllib.urlopen` to use a different context that bypasses TLS verification.

Another important project decision is to implement all wrappers using only the [Python Standard Library](https://docs.python.org/3/library/).


## Tests
Run tests with:

```
$ python -m unittest tests.test_prime_api
$ python -m unittest tests.test_netbox_api
$ python -m unittest tests.test_qradar_api
$ python -m unittest tests.test_hibp_api
$ python -m unittest tests.test_vt_api
$ python -m unittest tests.test_ise_api
$ python -m unittest tests.test_rdap_api
```
