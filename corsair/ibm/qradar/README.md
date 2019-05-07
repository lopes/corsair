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


## Basic Usage

```python
>>> from corsair.ibm.qradar import Api
>>> qradar = Api('https://qradar.corp/api', '4-53cur3-tok3n-h3r3')
>>>
>>> searches = qradar.ariel.read('searches')
>>> qradar.ariel.read(f'searches/{searches[0]}')
>>> qradar.ariel.read(f'searches/{searches[0]}/results')
>>>
>>> offenses = qradar.siem.read('offenses') 
>>> qradar.siem.read(f'offenses/{offenses[0]["id"]}')
>>>
>>> qradar.searches.create(query_expression='select * from flows last 5 minutes')
>>> qradar.system.read('servers')
```
