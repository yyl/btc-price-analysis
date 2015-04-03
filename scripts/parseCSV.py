#!/usr/bin/pythn

import pandas as pd
import os
import sys
import secrets
import xml.etree.cElementTree as ET
import csv
# config info
os.chdir(secrets.ROOT)
### filenames and paths
output_dir = "./data"
nyt_name = "nyt_internet.csv"
nyt_file = os.path.join(output_dir, nyt_name)
nyt_news_file = "nyt_news_only.csv"
nyt_news_only = os.path.join(output_dir, nyt_news_file)
### the output file name is the same as the input file, but with additional extension xml
nyt_xml = os.path.join(output_dir, nyt_news_file + ".xml")
merged_output = os.path.join(output_dir, nyt_name.split(".")[0] + "_with_score.csv")

### method to stdout news headlines only
def getHeadline():
    data = pd.read_csv(nyt_file, names=["time","headline"]).iloc[:,1:]
    data.to_csv(nyt_news_only, header=False, index=False, line_terminator=". ")

### method to merge sentiment score
def mergeSentiScore():
    # parse xml output of sentiment analysis
    tree = ET.parse(nyt_xml)
    root = tree.getroot()
    attr_g = (s.attrib for s in root[0][0])
    score = pd.DataFrame([attrs for attrs in attr_g])
    # lose the id column
    score = score.iloc[:,1:]
    # read in news data
    news_data = pd.read_csv(nyt_file, names=["time","headline"])
    # merge and output to csv file
    merged = pd.merge(news_data, score, left_index=True, right_index=True, how="left")
    merged.to_csv(merged_output, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: python parseCSV.py command_index"
        print "command_index:"
        print "        1: getHeadline()"
        print "        2: mergeSentiScore()"
        exit()
    param = int(sys.argv[1])
    if param == 1:
        getHeadline()
    elif param == 2:
        mergeSentiScore()
