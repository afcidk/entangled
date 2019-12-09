#!/usr/bin/env python3.7
import requests

BASE = 'https://api.thetangle.org/search/'

with open('/home/afcidk/entangled/address.txt', 'r') as f:
    lines = f.read().split('\n')

for line in lines:
    addr, start_timestamp = line.split()
    start_timestamp = int(start_timestamp)
    r = requests.get(BASE + addr)
    json = r.json()
    txs = [x['hash'] for x in json['bundle']['attachments'][0]['outputs']]
    print('============================')
    print(f'Bundle: {addr}')

    max_timestamp = -1
    for tx in txs:
        r = requests.get(BASE + tx)
        json = r.json()
        status = json['transaction']['status']

        if status == 'confirmed':
            timestamp = json['transaction']['confirmingTimestamp']
            max_timestamp = max(max_timestamp, timestamp)
            #print(tx, timestamp)
        else:
            print('Not confirmed')
            max_timestamp = -1
            break

    if max_timestamp > 0:
        print(f'Size: {len(txs)}, time: {max_timestamp-start_timestamp}s')
