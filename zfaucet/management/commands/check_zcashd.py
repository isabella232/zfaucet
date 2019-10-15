from django.core.management.base import BaseCommand, CommandError
from pyZcash.rpc.ZDaemon import *
import time
import sys

class Command(BaseCommand):
    help = 'Check for zcashd rpc'

    def add_arguments(self, parser):
        parser.add_argument('-w', '--wait', type=int, 
        help='Seconds to wait for zcashd rpc')

    def handle(self, *args, **kwargs):
        wait = kwargs['wait']
        timer = 0
        zd = ZDaemon()
        self.stdout.write('Checking for zcashd at {}'.format(zd.network) )
        while timer < wait:
            time.sleep(1)
            timer += 1
            try:
                zd.getNetworkHeight()
                height = zd.getNetworkHeight()
                assert type(height) is int
                return
            except (requests.exceptions.ConnectionError,AssertionError):
                pass
            self.stdout.write('Waiting {:d}s, elapsed {:d}s'.format(wait, timer) )
        self.stderr.write('Unable to connect to zcash at: {} within {:d}s'.format(zd.network, wait))
        sys.exit(1)

