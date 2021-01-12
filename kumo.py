#!/usr/bin/env /usr/bin/python

# Forked from https://github.com/szumlins/Scripts on Jan 12, 2021
# Adapted to Python 3

'''
This script is a simple tool to automate getting and setting of KUMO cross points via python
On get success, the script returns the source 
On set success, the script returns the source and destination separated by a comma
On failure, the script returns an error code
-1: can't connect to KUMO (check your URL)
-2: destination out of range (not enough destinations in router)
-3: source is out of range (not enough sources in router)
Requires installation of Requests module, can be installed with 'pip install requests'
'''

import requests
import argparse
import json
import sys

parser = argparse.ArgumentParser(
    description='Set and Get AJA KUMO cross points. On get success, the script returns the source. On set success, the script returns the source and destination separated by a comma. On failure, the script returns -1')
parser.add_argument('-d', '--get_xpt', dest='dest', metavar="CROSSPOINT", type=int, nargs=1,
                    help="Get crosspoint source for destination")
parser.add_argument('-s', '--set_xpt', dest='source', metavar="CROSSPOINT", type=int, nargs=1,
                    help="Set crosspoint source for destination (defined by -d)")
parser.add_argument('-a', '--address', dest='kumo', metavar="ADDRESS", type=str, nargs=1,
                    help="IP address or DNS name of KUMO")
args = parser.parse_args()


def error(code):
    if code == 1:
        sys.exit("ERROR: Can't connect to KUMO (check your URL or network)")
    elif code == 2:
        sys.exit('ERROR: destination out of range (not enough destinations in router)')
    elif code == 3:
        sys.exit('ERROR: source is out of range (not enough sources in router)')


if args.dest is None:
    sys.exit("No destination defined, exiting.")

if args.kumo is None:
    sys.exit("No router defined, exiting.")

# set our Kumo URL
kumo = 'http://' + args.kumo[0] + '/options'

# get Kumo source count (sc)
try:
    r = requests.get(kumo + '?action=get&paramid=eParamID_NumberOfSources')
    j = json.loads(r.text)
    sc = j['value']
except requests.ConnectionError:
    print(error(1))

# get Kumo destination count (dc)
try:
    r = requests.get(kumo + '?action=get&paramid=eParamID_NumberOfDestinations')
    j = json.loads(r.text)
    dc = j['value']
except requests.ConnectionError:
    error(1)

# if there isn't a source set on the cli, simply look up the source of the supplied destination
if not args.source:
    # if destination is larger than router size, exit with error
    if args.dest[0] > int(dc):
        error(2)

    # try getting source for defined destination
    try:
        r = requests.get(
            kumo + '?action=get&paramid=eParamID_XPT_Destination' + str(args.dest[0]) + '_Status',
            timeout=0.2)
    except requests.ConnectionError:
        error(1)

    j = json.loads(r.text)
    # if we get an error, print it, other wise print out source
    if j['value'] == '-1':
        error(2)
    else:
        print(j['value'])

else:
    # if source is larger than router size, exit with error
    if args.source[0] > int(sc):
        error(3)

    # there is a source defined, so switch it
    post_data = {
        'paramName': 'eParamID_XPT_Destination' + str(args.dest[0]) + '_Status',
        'newValue': str(args.source[0])
    }

    try:
        r = requests.post(kumo, data=post_data, timeout=0.2)
    except requests.ConnectionError:
        error(1)

    j = json.loads(r.text)

    # if we have an error, just return -2, if not return source,destination
    if j['value'] == '-1':
        error(2)
    else:
        print(j['value'] + ',' + str(args.dest[0]))
