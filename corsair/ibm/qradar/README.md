# Corsair > IBM > QRadar
The [IBM QRadar](https://www.ibm.com/security/security-intelligence/qradar) API wrapper uses `https://qradar.corp/api_docs` as its base.

Prerequisites:

* QRadar 7.3.0
* API 8.0
* Access credentials (token)

An example on how QRadar structures URLs and how it's mapped in Corsair follows:

```
https://qradar.corp/api/ariel/searches/22d21cc3-7ea9-4bad-96f8-a652e21b7743/results
\_____________________/\____/\____________________________________________/\______/
      Base URL        Endpoint                  Resource                    Suffix
```

QRadar paginates using HTTP headers, so Corsair implemented the keyword `Range` whose value is inserted in request's header to ask for certain number of items.  The syntax used is `items=F-L`, where `F` and `L` are the indexes of first and last items (doesn't include the last index), like this: `Range='items=90-200'` (will retrieve from 90 to 199).  The response headers contain the `Content-Range` field, which has the original request range and the number of items, like this: `items 90-200/917`.  Remember that indexes start at position 0 and that there's no problem on asking for a non-existent index, because QRadar will handle it appropriately.  To deal with this behaviour, method `read` will return a tuple with the results at position 0 and the paging data at position 1.


## Basic Usage

```python
>>> from corsair.ibm.qradar import Api
>>> qradar = Api('https://qradar.corp/api', '4-53cur3-tok3n-h3r3')
>>>
>>> searches = qradar.ariel.read('searches')[0]
>>> qradar.ariel.read(f'searches/{searches[0]}')
>>> qradar.ariel.read(f'searches/{searches[0]}/results')
>>>
>>> offenses = qradar.siem.read('offenses')[0]
>>> qradar.siem.read(f'offenses/{offenses[0]["id"]}')
>>> qradar.siem.read('offenses', Range='items=4-5')
>>>
>>> qradar.searches.create(query_expression='select * from flows last 5 minutes')
>>> qradar.system.read('servers')
```
