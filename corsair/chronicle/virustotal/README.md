# Corsair > Chronicle > VirusTotal
This [VirusTotal](https://virustotal.com) API wrapper is based in the official developer guide, available at `https://developers.virustotal.com/reference`.

Prerequisites:

* API v2
* 1 request by 15 seconds

An example on how VirusTotal structures URLs and how it's mapped in Corsair follows:

```
https://www.virustotal.com/vtapi/v2/file/scan/upload_url?apikey=alongapikey
\_________________________________/\____/\___/\________/\_________________/
           Base URL              Endpoint Resource Suffix     Filters
```

Thanks to VirusTotal for providing private API access to implement this wrapper.  The only endpoints I couldn't test due to lack of permissions were `file/feed`, `url/scan`, `url/feed`, and `comments/put`


## Basic Usage

```python
>>> from corsair.chronicle.virustotal import Api
>>> vt = Api('https://www.virustotal.com/vtapi/v2', 'my-apikey')
>>> eicar = '3395856ce81f2b7382dee72602f798b642f14140'
>>>
>>> vt.file.read('report', resource=eicar, allinfo='true')
>>> vt.file.create('scan', file=open('README.md', 'rb'))
>>> vt.file.read('scan/upload_url')
>>> vt.file.read('download', hash=eicar, output_file='foo.bin')
>>> vt.file.read('behaviour', hash=eicar)
>>> vt.file.read('network-traffic', hash=eicar)
>>> vt.file.read('clusters', date='2019-05-01')
>>>
>>> results = vt.file.read('search', query='eicar')
>>> vt.file.read('search', query='eicar', offset=results['offset'])
>>>
>>> vt.url.read('report', resource='http://www.my-homepage.com', scan='1')
>>> vt.domain.read('report', domain='virustotal.com')
>>> vt.ip_address.read('report', ip='200.1.2.3')
>>>
>>> c1 = vt.comments.read('get', resource=eicar)
>>> c2 = vt.comments.read('get', resource=eicar, before=c1['comments'][-1]['date'])
```
