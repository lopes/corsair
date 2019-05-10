#!/usr/bin/env python3
# Reads all devices and access points in Prime, and all IP addresses
# in NetBox.  If a device is in Prime and not in NetBox, it'll be
# created, else, if NetBox description is different from hostname
# in Prime, it'll be updated.
#
# This script puts the tag defined in prime_tag for all IP addresses
# present in Prime.  It'll also check all IP addresses in NetBox
# with tag prime_tag that aren't in Prime, then delete them.
#
# Usage:
# $ python sync_prime_netbox.py
# 
# Author: José Lopes
# License: MIT
##


import re

from time import sleep

from corsair.cisco.prime import Api as Prime
from corsair.digitalocean.netbox import Api as Netbox


prime = Prime('', '', '')
netbox = Netbox('', '')
prime_tag = 'prime'
wait = 1  # seconds


def get_all_prime_devices():
    'Returns a list of Prime Devices and Access Points [(IP,Hostname),...]'
    devices = dict()
    raw = get_all_prime('Devices')
    for device in raw:
        try:
            devices.update({device['devicesDTO']['ipAddress']:
                device['devicesDTO']['deviceName']})
        except KeyError:
            print(f'ERROR: {device}')
    
    raw = get_all_prime('AccessPoints')
    for ap in raw:
        try:
            devices.update({ap['accessPointsDTO']['ipAddress']['address']:
                ap['accessPointsDTO']['model']})
        except KeyError:
            print(f'ERROR: {device}')
    return devices

def get_all_prime(resource):
    'This function is used to support get_all_prime_devices().'
    raw = list()
    res = prime.data.read(resource, full='true')
    count = res['queryResponse']['@count']
    last = res['queryResponse']['@last']
    raw.extend(res['queryResponse']['entity'])
    while last < count - 1:
        first_result = last + 1
        last += 1000  # default number of results set in Corsair for Prime
        res = prime.data.read(resource, full='true', firstResult=first_result)
        raw.extend(res['queryResponse']['entity'])
    return raw


def get_all_netbox_addresses():
    addrs, raw = (dict(), list())
    res = netbox.ipam.read('ip-addresses')
    raw.extend(res['results'])
    while res['next']:
        offset = int(re.sub(r'^.*offset=([0-9]+).*$', r'\1', res['next']))
        res = netbox.ipam.read('ip-addresses', offset=offset)
        raw.extend(res['results'])
    for addr in raw:
        addrs.update({addr['address']: (addr['id'], addr['description'], addr['tags'])})
    return addrs



if __name__ == '__main__':
    prime_devices = get_all_prime_devices()
    netbox_addresses = get_all_netbox_addresses()

    for k,v in prime_devices.items():
        if f'{k}/32' not in netbox_addresses:
            sleep(wait)
            netbox.ipam.create('ip-addresses', address=k, description=v, tags=[prime_tag])
            print(f'CREATED: {k} ({v}) [prime]')
        else:
            if v != netbox_addresses[f'{k}/32'][1]:
                sleep(wait)
                netbox.ipam.update(f'ip-addresses/{netbox_addresses[f"{k}/32"][0]}',
                    description=v, tags=[prime_tag])
                print(f'UPDATED: {k} ({v}) [prime]')
            elif prime_tag not in netbox_addresses[f'{k}/32'][2]:
                sleep(wait)
                netbox.ipam.update(f'ip-addresses/{netbox_addresses[f"{k}/32"][0]}',
                    tags=[prime_tag])
                print(f'UPDATED: {k} ([prime])')
    
    for k,v in netbox_addresses.items():
        if (prime_tag in v[2]) and (k.split('/')[0] not in prime_devices):
            sleep(wait)
            netbox.ipam.delete(f'ip-addresses/{v[0]}')
            print(f'DELETED: {k.split("/")[0]} ({v[0]})')
