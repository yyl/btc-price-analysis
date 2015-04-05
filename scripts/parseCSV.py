#!/usr/bin/pythn

import pandas as pd
import os
import sys
import secrets
import xml.etree.cElementTree as ET
import csv
# config info
os.chdir(secrets.ROOT)
output_dir = "./data"

### method to stdout news headlines only
def getHeadline(nyt_path, nyt_news_only_path):
    data = pd.read_csv(nyt_path, names=["time","headline"]).iloc[:,1:]
    data.to_csv(nyt_news_only_path, header=False, index=False, line_terminator=". ")

### method to merge sentiment score
def mergeSentiScore(nyt_path, nyt_xml_path, merged_output_path):
    # parse xml output of sentiment analysis
    tree = ET.parse(nyt_xml_path)
    root = tree.getroot()
    attr_g = (s.attrib for s in root[0][0])
    score = pd.DataFrame([attrs for attrs in attr_g])
    # lose the id column
    score = score.iloc[:,1:]
    # read in news data
    news_data = pd.read_csv(nyt_path, names=["time","headline"])
    # merge and output to csv file
    merged = pd.merge(news_data, score, left_index=True, right_index=True, how="left")
    merged.to_csv(merged_output_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python parseCSV.py command_index filename"
        print "command_index:"
        print "                1: getHeadline()"
        print "                2: mergeSentiScore()"
        print "filename:       the name of input file"
        exit()
    param = int(sys.argv[1])
    ## parse and generate paths to file
    ## nyt_name is the filename of raw news data
    nyt_name = sys.argv[2]
    ## nyt_paths is the path to nyt_name file
    nyt_path = os.path.join(output_dir, nyt_name)
    ## file containing news headline only
    nyt_news_only = "news_only_" + nyt_name
    ## path to nyt_news_only file
    nyt_news_only_path = os.path.join(output_dir, nyt_news_only)
    ## trigger getHeadline function
    if param == 1:
        getHeadline(nyt_path, nyt_news_only_path)
    ## trigger mergeSentiScore function
    elif param == 2:
        ## the output file name is the same as the input file, but with additional extension xml
        ## output file of sentiment score algorithm
        nyt_xml_path = os.path.join(output_dir, nyt_news_only + ".xml")
        ## the path of the merged output
        merged_output_path = os.path.join(output_dir, nyt_name.split(".")[0] + "_with_score.csv")
        mergeSentiScore(nyt_path, nyt_xml_path, merged_output_path)
