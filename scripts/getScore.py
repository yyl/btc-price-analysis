#!/usr/bin/python
import os
import pandas as pd
import numpy as np
import indicoio
import secrets
os.chdir(secrets.ROOT)
output_dir = "./data"
input_dir = "./data"

def getIndico(news_file):
    output_file_name = "indico_" + news_file
    news_data = pd.read_csv(os.path.join(input_dir, news_file), names=["time","headline"])
    news_data['indico_score'] = np.vectorize(lambda x: indicoio.sentiment(x))(news_data.headline)
    news_data.to_csv(os.path.join(output_dir, output_file_name), index=False)

getIndico("nyt_bitcoin.csv")
