# Corsair > Troy Hunt > Have I Been Pwned
This [Have I Been Pwned](https://haveibeenpwned.com) (HIBP) API wrapper is based in `https://haveibeenpwned.com/API/v2`.

Prerequisites:

* API v2
* 1 request by 1.5 seconds

An example on how HIBP structures URLs and how it's mapped in Corsair follows:

```
https://haveibeenpwned.com/api/breach/500px
\____________________________/\______/\___/
           Base URL           Endpoint Resource
```

Its good to point that `breaches` and `breach` endpoints could be concatenated into a single `breaches` endpoint, and if the programmer informed a singular breach, it'd return that breach.  HIBP also have a `range` endpoint, but as it uses a completely different URL and returns data in a different format, I decided not to implement it.


## Basic Usage

```python
>>> from corsair.troyhunt.haveibeenpwned import Api
>>> hibp = Api('https://haveibeenpwned.com/api')
>>>
>>> hibp.breachedaccount.read('me@domain')
>>> hibp.breachedaccount.read('me@domain', truncateResponse='true', includeUnverified='true')
>>> hibp.breaches.read('')
>>> hibp.breaches.read('', domain='linkedin.com')
>>> hibp.breach.read('500px')
>>> hibp.dataclasses.read('')
>>> hibp.pasteaccount.read('me@domain')
```
