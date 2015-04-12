#!/usr/bin/python
import pandas as pd
import datetime
import numpy as np
import scipy as sp
import os
import matplotlib.pyplot as plt
import matplotlib
import scriptine
os.chdir("/root/Envs/btc-project/btc-price-analysis")

##### constants
time_format = "%Y-%m-%dT%H:%M:%S"

def parseWeek(w):
	"""parse data from google trend"""
	return w.split(" - ")[1]

def truthLabel(cur,prev):
	"""add rise/fall groundtruth label to price data"""
	if cur == prev:
	    return 0
	elif cur > prev:
	    return 1
	else:
	    return -1

def googletrend_preprocess():
	"""preprocessing step of google trend classifier; return a DataFrame"""
	## read search interest index (SII) data
	trend = pd.read_csv("./data/trend.csv", converters={0:parseWeek})
	trend['Week'] = pd.to_datetime(trend['Week'])
	trend.set_index(['Week'], inplace=True)
	trend.columns = ['search']
	## read bitcoin price data
	data = pd.read_csv("./data/price.csv", names=['time', 'price'], index_col='time',
	                   parse_dates=[0], date_parser=lambda x: datetime.datetime.strptime(x[:-6], time_format))
	bpi = data.resample('w-sat', how='ohlc')
	bpi.index.name = 'Week'
	## use weekly close price only
	bpi = pd.DataFrame(bpi['price']['close'])
	## merge two datasets
	trend_bpi = pd.merge(trend, bpi, how='right', left_index=True, right_index=True)
	trend_bpi.columns = ['SII', 'close_price']
	trend_bpi = trend_bpi['2012':]
	## add ground truth label to weekly price
	trend_bpi['truth'] = np.vectorize(truthLabel)(trend_bpi.close_price, trend_bpi.close_price.shift(1))
	return trend_bpi

def googletrend(data, delta_t, diff, inverse=False):
	"""rule-based classifier with google trend search data. Search index rises => price will fall next week.

    Keyword arguments:
    data -- DataFrame used to generate prediction
    delta_t -- the number of weeks in calculating rolling_SII
    diff -- the threshold of difference between current SII and previous rolling SII
    inverse -- change the algorithm so that search index rises => price will rise next week
    """
	## compute rolling mean of SII given delta_t
	data['rolling_SII'] = pd.rolling_mean(data.SII, delta_t)
	## shift rolling mean one week ahead
	data['rolling_SII_shifted'] = data.rolling_SII.shift(1)
	## calculate difference of current SII and rolling SII (shifted)
	data['SII_diff'] = data.SII - data.rolling_SII_shifted
	## generate prediction, which is also order signal
	data['order'] = 0
	if not inverse:
		## SII_diff >= diff => search interest rises this week => price rises next week
		data.loc[data.SII_diff >= diff, 'order'] = -1
		## SII_diff < diff => search interest falls this week => price falls next week
		data.loc[data.SII_diff < diff, 'order'] = 1
	else:
		## SII_diff >= diff => search interest rises this week => price rises next week
		data.loc[data.SII_diff >= diff, 'order'] = 1
		## SII_diff < diff => search interest falls this week => price falls next week
		data.loc[data.SII_diff < diff, 'order'] = -1		
	#return data

def googletrend_evaluate(trend_bpi):
	"""return true positive rate anf false positive rate"""
	## calculate evaluation metric
	## price rise as positive class, fall as negative
	true_positive = trend_bpi[(trend_bpi.truth==1)&(trend_bpi.order==1)].order.count()
	false_negative = trend_bpi[(trend_bpi.truth==1)&(trend_bpi.order==-1)].order.count()
	false_positive = trend_bpi[(trend_bpi.truth==-1)&(trend_bpi.order==1)].order.count()
	true_negative = trend_bpi[(trend_bpi.truth==-1)&(trend_bpi.order==-1)].order.count()
	## true positive rate and false positive rate (used to plot ROC)
	tp_rate = float(true_positive) /(true_positive+false_negative)
	fp_rate = float(false_positive) /(true_negative+false_positive)
	# print "TPR: %f, FPR: %f" % (tp_rate, fp_rate)
	return tp_rate, fp_rate