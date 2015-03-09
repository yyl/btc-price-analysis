#!/usr/bin/python

import requests
from datetime import datetime, timedelta
import re

REQUEST = "https://api.coinbase.com/v1/prices/historical"
MARKET_REQUEST = "https://api.exchange.coinbase.com/products/BTC-USD/candles"
INIT = '2015-01-01T00:00:00'
BUCKET_SIZE = 5
GRANULARITY = 86400
DT_FORMAT = "%Y-%m-%dT%H:%M:%S"

def price():
    with open("./data.csv", "a+") as f:
        for i in xrange(1, 180):
            print "page %d..." % i
            param = {'page': i}
            r = requests.get(REQUEST, params=param)
            if r.status_code == 200:
                f.write(r.text+"\n")

# volume and price data from Exchange API
# https://api.exchange.coinbase.com/products/BTC-USD/candles?start=2015-03-04T12:43:20&end=2015-03-08T12:45:20&granularity=86400
def marketData():
    init = datetime.strptime(INIT, "%Y-%m-%dT%H:%M:%S")
    bucket = timedelta(days=BUCKET_SIZE)
    with open("./market.csv", "w+") as marketf:
        param = {'granularity':GRANULARITY}
        for i in xrange(5):
            start_datetime = init + bucket*i
            end_datetime = start_datetime + bucket - timedelta(seconds=1)
            param['start'] = start_datetime.strftime(DT_FORMAT)
            param['end'] = end_datetime.strftime(DT_FORMAT)
            print param
            r = requests.get(MARKET_REQUEST, params=param)
            if r.status_code == 200:
                matches = re.findall(r'\[([\d.,]+?)\]', r.text)
                for entry in (m.split(',') for m in matches):
                    bucket_t = datetime.fromtimestamp(long(entry[0])). \
                                            strftime(DT_FORMAT)
                    print bucket_t, entry[-2], entry[-1]
                    #marketf.write("%s,%s,%s\n" % (bucket_t, entry[-2], entry[-1]))

if __name__ == '__main__':
    marketData()
