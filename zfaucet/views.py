from django.http import JsonResponse
from django.utils import timezone as django_tz
from  zfaucet.settings import DONATION_ORG

import re
from datetime import *

from pyZcash.rpc.ZDaemon import *

zd = ZDaemon(network=ZCASH_NETWORK)

def donations(request):
    data = {}
    data['org'] = DONATION_ORG
    data['t_address'] = find_taddr_with_unspent()
    data['z_address_legacy'] = find_z_sapling_address()
    data['z_address_sapling'] = find_z_legacy_address()
    return JsonResponse(data)

def find_taddr_with_unspent():
    zd = ZDaemon(network=ZCASH_NETWORK)
    for utxo in zd.listunspent():
        if utxo['spendable'] == True and utxo['amount'] > 0.1:
            return utxo['address']

def find_z_sapling_address():
    zd = ZDaemon(network=ZCASH_NETWORK)
    for z_addr in zd.z_listaddresses():
        if z_addr.startswith('zt') and not z_addr.startswith('ztestsapling'):
            return z_addr

def find_z_legacy_address():
    zd = ZDaemon(network=ZCASH_NETWORK)
    for z_addr in zd.z_listaddresses():
        if z_addr.startswith('ztestsapling'):
            return z_addr