#!/usr/bin/env python3
# This script uploads large files (between 32 and 200 MB) to
# VirusTotal for further analysis.
#
# Usage:
# $ python vt-uploader.py file
# 
# Author: José Lopes
# License: MIT
##

from sys import argv
from pprint import pprint
from time import sleep

from requests import post

from corsair.chronicle.virustotal import Api


vt_apikey = ''
vt_apiurl = 'https://www.virustotal.com/vtapi/v2'
wait_time = 20  # seconds


if __name__ == '__main__':
    with open(argv[1], 'rb') as f:
        vt = Api(vt_apiurl, vt_apikey)
        upload_url = vt.file.read('scan/upload_url')['upload_url']
        res = post(upload_url, files={'file': (argv[1], f)})
        sha1 = res.json()['sha1']
        
        scan = vt.file.read('report', resource=sha1, allinfo='true')
        while scan.get('response_code', 0) != 1:
            sleep(wait_time)
            scan = vt.file.read('report', resource=sha1, allinfo='true')
        pprint(scan)
