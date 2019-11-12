#!env python3

import argparse
import socket
import time
import sys

waiting = True
elasped = 0

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Host to test")
parser.add_argument("--port", help="Port to test", type=int)
parser.add_argument("--timeout", help="Seconds to wait (default 10)", type=int, default=10 )
args = parser.parse_args()
print('waiting for: {}:{}'.format(args.host, args.port))

while waiting:
    if elasped > args.timeout:
        print('Timeout reached, exiting')
        sys.exit(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((args.host, args.port))
        waiting = False
    except socket.error:
        elasped += 2
        time.sleep(2)
        print('Elapsed: {}s'.format(elasped))

print('Connect to {}:{}!'.format(args.host, args.port))