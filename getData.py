#!/usr/bin/python

import requests
from datetime import datetime, timedelta
import re
from dateutil import tz

# endpoint for historical price
REQUEST = "https://api.coinbase.com/v1/prices/historical"
### exchange API
# endpoint for historical market volume and price
MARKET_REQUEST = "https://api.exchange.coinbase.com/products/BTC-USD/candles"
# market data starting date
INIT = '2014-01-01T00:00:00'
# number of days in each request
BUCKET_SIZE = 100
# number of days to obtain
DATA_SIZE = 600
# number of requests given bucket size and data size
### two variables have to be divisible
REQUEST_SIZE = DATA_SIZE/BUCKET_SIZE
# interval of each entry in bucket
GRANULARITY = 86400
# datetime format for parsing
DT_FORMAT = "%Y-%m-%dT%H:%M:%S"
# output datetime format
OUT_FORMAT = "%Y-%m-%d"
# timezone objects
to_zone = tz.tzutc()
from_zone = tz.tzlocal()
# output file name
MARKET_FILE = './market.csv'

def price():
    with open("./data.csv", "a+") as f:
        for i in xrange(1, 180):
            print "page %d..." % i
            param = {'page': i}
            r = requests.get(REQUEST, params=param)
            if r.status_code == 200:
                f.write(r.text+"\n")

# volume and price data from Exchange API
# the data represents the exchanged volume and the close price for each day
def marketData():
    # initial start time
    init = datetime.strptime(INIT, "%Y-%m-%dT%H:%M:%S")
    # initialize bucket size
    bucket = timedelta(days=BUCKET_SIZE)
    with open(MARKET_FILE, "w+") as marketf:
        param = {'granularity':GRANULARITY}
        for i in xrange(5):
            # construct proper bucket
            # start time
            start_datetime = init + bucket*i
            param['start'] = start_datetime.strftime(DT_FORMAT)
            # end time
            end_datetime = start_datetime + bucket - timedelta(seconds=1)
            param['end'] = end_datetime.strftime(DT_FORMAT)
            # make request
            print "querying data of %s..." % param['start']
            r = requests.get(MARKET_REQUEST, params=param)
            if r.status_code == 200:
                # find all valid entries from string
                # then iterate each one
                matches = re.findall(r'\[([\d.,]+?)\]', r.text)
                for entry in reversed([m.split(',') for m in matches]):
                    # convert stored timezone to UTC
                    bucket_datetime = datetime.fromtimestamp(long(entry[0]))
                    bucket_datetime = bucket_datetime.replace(tzinfo=from_zone)
                    bucket_t = bucket_datetime.astimezone(to_zone).strftime(OUT_FORMAT)
                    # write data to file
                    marketf.write("%s,%s,%s\n" % (bucket_t, entry[-2], entry[-1]))

if __name__ == '__main__':
    marketData()
