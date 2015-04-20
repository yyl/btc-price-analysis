#!/usr/bin/python
import pandas as pd
import datetime
import numpy as np
import scipy as sp
import os
import matplotlib.pyplot as plt
import matplotlib
import scriptine
import datetime
## non-standard import
import secrets
from alchemyapi import AlchemyAPI
## env config
os.chdir(secrets.ROOT)
output_dir = "./data"
input_dir = "./data"

def alchemy_score(x):
	"""Calling Alchemy API to calculate sentiment score."""
	alchemyapi = AlchemyAPI()
	response = alchemyapi.sentiment("text", x)
	return response["docSentiment"].get("score", 0.0)

def preprocess(news_path):
	"""Get sentiment score from Alchemy for news data in news_path."""
	print "computing sentiment score using AlchemyAPI for %s..." % news_path
	output_file_name = "alchemy_" + os.path.basename(news_path)
	news_data = pd.read_csv(news_path, names=["time","headline"])
	news_data['alchemy_score'] = np.vectorize(alchemy_score)(news_data.headline)
	news_data.to_csv(os.path.join(output_dir, output_file_name), index=False)

def interpolate_news(news_file):
	"""Give each piece of news a 'price' to fit in the BTC price graph.
	Return a new file with price interpolated based on original price data.

	Keywords:
	news_file -- file path to the news data with sentiment score
	"""
	prefix = "interpolated_"
	time_format = "%Y-%m-%dT%H:%M:%SZ"
	news_data = pd.read_csv(news_file,
						header=True, names=['time', 'headline', 'score'],
						index_col=0, parse_dates=[0], 
						date_parser=lambda x: datetime.datetime.strptime(x, time_format)) \
			.drop_duplicates(take_last=True) \
			.iloc[::-1] # reverse the original order of index
	## create new DF for interpolating
	news_index = news_data[:]
	news_index.loc[:,'price'] = None
	news_index.drop('headline', axis=1, inplace=True)
	news_index.drop('score', axis=1, inplace=True)
	## column to mark rows from news_file
	news_index.loc[:,'bit'] = 1
	## read in price data and remove duplicates
	time_format = "%Y-%m-%dT%H:%M:%S"
	raw_price = pd.read_csv(os.path.join(input_dir, "price.csv"), names=['time', 'price'], 
						index_col='time', parse_dates=[0], 
						date_parser=lambda x: datetime.datetime.strptime(x, time_format))
	raw_price['time_index'] = raw_price.index
	raw_price.drop_duplicates(subset='time_index', take_last=True, inplace=True)
	del raw_price['time_index']
	## downsample price data to 12h
	price_data = pd.DataFrame(raw_price.resample('12h', how='ohlc').ix[:, 3])
	price_data.columns = ['price']
	## concatenate news data with price data
	news_filled = pd.concat([news_index, price_data]).sort_index()
	## interpolate on price based on datetime index
	news_filled.loc[:,'price'].interpolate(method='time', inplace=True)
	## keep only news data by dropping empty bit rows
	news_filled.dropna(axis=0, inplace=True)
	## drop bit column too
	news_filled.drop('bit', axis=1, inplace=True)
	## add interpolated price data back to news data
	news_price = pd.merge(news_filled, news_data, how='left', left_index=True, right_index=True)
	## output to file
	output_file = prefix + os.path.basename(news_file)
	news_price.to_csv(os.path.join(output_dir, output_file))

def algorithm():
	"""Perform classification based on sentiment score"""
	pass