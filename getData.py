#!/usr/bin/python

import requests

REQUEST = "https://api.coinbase.com/v1/prices/historical"


with open("./data.csv", "a+") as f:
    for i in xrange(1, 101):
        print "page %d..." % i
        param = {'page': i}
        r = requests.get(REQUEST, params=param)
        if r.status_code == 200:
            f.write(r.text)
