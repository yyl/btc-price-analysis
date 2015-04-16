#!/usr/bin/python
import pandas as pd
import datetime
import numpy as np
import scipy as sp
import os
import matplotlib.pyplot as plt
import matplotlib
import scriptine
## non-standard import
import secrets
from alchemyapi import AlchemyAPI
## env config
os.chdir(secrets.ROOT)
output_dir = "./data"
input_dir = "./data"

def alchemy_score(x):
	alchemyapi = AlchemyAPI()
	response = alchemyapi.sentiment("text", x)
	return response["docSentiment"].get("score", 0.0)


def preprocess(news_file):
	"""Get sentiment score from Alchemy"""
	print "computing sentiment score using AlchemyAPI for %s..." % news_file
	output_file_name = "alchemy_" + news_file
	news_data = pd.read_csv(os.path.join(input_dir, news_file), names=["time","headline"])
	news_data['alchemy_score'] = np.vectorize(alchemy_score)(news_data.headline)
	news_data.to_csv(os.path.join(output_dir, output_file_name), index=False)

def algorithm():
	"""Perform classification based on sentiment score"""
	pass

preprocess("nyt_bitcoin.csv")