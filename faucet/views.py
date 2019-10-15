from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone

import re
from datetime import *

from pyZcash.rpc.ZDaemon import *
from faucet.models import *


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('HTTP_X_REAL_IP')
    return ip

def index(request):
    # TODO: Going to show the page no matter what, so pull these variables out.
    if HealthCheck.objects.latest('timestamp'):
        hc = HealthCheck.objects.latest('timestamp')
        t_balance = hc.t_balance
        z_balance = hc.z_balance
        print('T balance'.format(t_balance))
        print('z balance"'.format(z_balance))
        balance = {'transparent': t_balance, 'private': z_balance}
        difficulty = hc.difficulty
        height = hc.height
        payouts = Drip.objects.count()
    else:
        balance = '0'
        difficulty = '0'
        height = '0'

    zd = ZDaemon(network=ZCASH_NETWORK)
    version = zd.getVersion()

    #If it is a post, an address was submitted.
    if request.method == 'POST':
        # Check IP and payout address
        # This is the old workaround, added get_client_ip
        ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1':
            ip = request.META.get('HTTP_X_REAL_IP')
        ip = get_client_ip(request)
        address = request.POST.get('address', '')
        print('client IP: {}'.format(ip))
        print('client address: {}'.format(address))
        try:
            last_payout = Drip.objects.filter(Q(ip=ip) | Q(address=address)).order_by('-timestamp')[0]
            now = datetime.utcnow().replace(tzinfo=timezone.get_current_timezone())
            timesince = (now - last_payout.timestamp).total_seconds()

            # TODO: keep track of sessions as well, track one per session?

            if timesince < (60*60*12):
                msg = "Sorry, you received a payout too recently.  Come back later."
                return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})

        except (Drip.DoesNotExist, IndexError) as e:
            # Nothing in queryset, so we've never seen this ip and address before (individually)
            pass

        # zd = ZDaemon()
        try:
            # Did the tx work?
            # Transparent address
            if len(address) == len('tmKBPqa8qqKA7vrGq1AaXHSAr9vqa3GczzK'):
                tx = zd.sendtoaddress(address, 1.0)
                if len(tx) == len('2ac64e297e3910e7ffda7210e7aa2463fe2ec5f69dfe7fdf0b4b9be138a9bfb8'):
                    #Save Drip.
                    drip = Drip(address=address,txid=tx,ip=ip)
                    drip.save()
                    msg = "Sent! txid: {0}. View your transaction on the testnet explorer.".format(tx)
                    return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})
            # Sapling address
            elif len(address) == len('ztestsapling1603ydy9hg79lv5sv9pm5hn95cngfv4qpd6y54a8wkyejn72jl30a4pfhw8u00p93mu4nj6qxsqg'):
                print('Received a Sapling address')
                # sender = 'ztestsapling1603ydy9hg79lv5sv9pm5hn95cngfv4qpd6y54a8wkyejn72jl30a4pfhw8u00p93mu4nj6qxsqg'
                zaddrs = zd.z_listaddresses()
                sender = zaddrs[1]
                msg = 'Thanks for using zfaucet!'
                opid = zd.z_sendmany(sender, address, 1.0, msg)
                print('OPID: {}'.format(opid))
                if opid != None and 'opid' in opid:
                        resp = zd.z_getoperationstatus(opid)
                        print('Operation status response: {}'.format(resp))
                        print('operation status: {}'.format(resp[0]['status']))
                        #why is it not working when it's executing?
                        if resp[0]['status'] == 'executing':
                            msg = "Sent! You should receive your Sapling funds shortly."
                            return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})
                        if resp[0]['status'] == 'failed':
                            msg = "Operation failed for {0}. Error message: {1}".format(opid, resp[0]['error']['message'])
                            return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})
            # Sprout
            elif len(address) == len('ztSwdDwPhpUZ447YU1BqjxrvutHfu2AyENwUohhTMhnWHreAEHTELhRLvqkARmCSudW1GAcrg58TVaqT7oTH1ohFA7k7V11'):
                # sender = 'ztSwdDwPhpUZ447YU1BqjxrvutHfu2AyENwUohhTMhnWHreAEHTELhRLvqkARmCSudW1GAcrg58TVaqT7oTH1ohFA7k7V11'
                print('Received a Sprout address')
                zaddrs = zd.z_listaddresses()
                sender = zaddrs[0]
                msg = 'Thanks for using zfaucet!'
                opid = zd.z_sendmany(sender, address, 1.0, msg)
                print('OPID: {}'.format(opid))
                if opid != None and 'opid' in opid:
                        resp = zd.z_getoperationstatus(opid)
                        print('Operation status response: {}'.format(resp))
                        print('operation status: {}'.format(resp[0]['status']))
                        #why is it not working when it's executing?
                        if resp[0]['status'] == 'executing':
                            msg = "Sent! You should receive your Sprout funds shortly."
                            return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})
                        if resp[0]['status'] == 'failed':
                            msg = "Operation failed for {0}. Error message: {1}".format(opid, resp[0]['error']['message'])
                            return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})
        except:
            # TODO: Give better error if faucet is empty!
            print('ERROR: unknow address format')
            msg = "Issue sending transaction.  Is your address correct?"
            return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})


    return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':False, 'message':""})
