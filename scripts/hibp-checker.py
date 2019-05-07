#!/usr/bin/env python3
# This script receives a file with one email address per line
# and tests each one against Have I Been Pwned to find any
# leaks, using Corsair's HIBP wrapper.
#
# $ cat users.txt
# user1@domain
# user2@domain
# ...
#
# Usage:
# $ python hibp-checker.py users.txt
# 
# Author: José Lopes
# License: MIT
##

from sys import argv
from time import sleep

from corsair.troyhunt.haveibeenpwned import Api
from corsair import CorsairError


hibp = Api('https://haveibeenpwned.com/api')


def get_leaks(mail):
    ret = {'mail': mail, 'leaks': list()}
    try:
        ba = hibp.breachedaccount.read(mail, truncateResponse='true', 
            includeUnverified='true')
    except CorsairError:
        return ret
    for n in ba:
        ret['leaks'].append(n['Name'])
    return ret
    

if __name__ == '__main__':
    with open(argv[1], 'r') as f:
        for mail in f.readlines():
            leak = get_leaks(mail[:-1])  # avoiding \n
            print('{:<40} {}'.format(leak['mail'], ', '.join(leak['leaks'])))
            sleep(2)  # being gentle to HIBP
