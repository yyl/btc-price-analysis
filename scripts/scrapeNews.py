#!/usr/bin/python
'''
The script to extract current news headlines
'''

import newspaper
import re
import secrets
import requests
import os
import sys
os.chdir("../")

### scrape news from various news sites through newspaper lib
### needs REDO
def bitcoin_news(news_url):
    url_file = 'data/urls.txt'
    cnn_source = newspaper.build(news_url, memoize_articles=False)
    print '\n====> Grab %d articles from %s' % (cnn_source.size(), news_url)
    ## extract urls
    article_urls = (article.url for article in cnn_source.articles)
    ## grab bitcoin news
    #searches = (re.search(r'.+\/(\d+?)\/(\d+?)\/(\d+?)\/.+bitcoin.+', url) for url in article_urls)
    searches = (re.search(r'.+bitcoin.+', url) for url in article_urls)
    news = (match.group(0) for match in searches if match)
    for d in news:
        print d
    '''
    ## find all dates
    search_dates = (re.search(r'\/(\d+?)\/(\d+?)\/(\d+?)\/', url) for url in article_urls)
    dates = ((match.group(1), match.group(2), match.group(3)) for match in search_dates if match)
    ## find only news with bitcoin in headline
    search_news = (re.search(r'.+bitcoin.+', url) for url in article_urls)
    bitcoin_news = (match.group(0) for match in search_news if match)
    for b in bitcoin_news:
        print b
    with open(url_file, 'a+') as f:
        for a_url in article_urls:
            f.write(a_url + '\n')
    '''

### scrape news from NYT through standard API
### topic: the keyword to search titles for
### topic could be a series of keywords connected with comma,
### which need to be parsed properly
def scrapeNYT(topic, filename):
    topics = topic.split(",")
    ## file to save news
    data_file = 'data/%s.csv' % filename
    nyt_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
    ## specify query start and end date
    bdate = '20120101'
    edate = '20151231'
    params = {
            'begin_date': bdate,
            'end_date':   edate,
            # filter based on Lucene syntax
            'fq':         'headline:("%s")' % '" "'.join(topics),
            'api-key':    secrets.NYT_API_KEY,
            'sort':       'oldest'}
    ## get the size of news first
    resp = requests.get(nyt_url, params=params)
    if resp.status_code == 200:
        resp_obj = resp.json()
        size = resp_obj['response']['meta']['hits']
        print "====> %s articles from %s to %s" % (size, bdate, edate)
        with open(data_file, 'w+') as f:
            ## page through all results
            p = 0
            while size > 0:
                params['page'] = p
                resp_page = requests.get(nyt_url, params=params)
                if resp_page.status_code == 200:
                    resp_obj = resp_page.json()
                    docs = resp_obj['response']['docs']
                    for d in docs:
                        f.write('%s,"%s"\n' % (d['pub_date'].encode('utf8'), d['headline']['main'].encode('utf8')))
                    p += 1
                    size -= len(docs)

if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[1] != "1":
        print ""
        print "============= script to scrape news from different sources ======="
        print "============="
        print "usage:        python scrapeNews.py method_id input_param file_name"
        print "method_id:    0 - google news (not working), 1 - NYT"
        print "input_param:  NYT - search keyword"
        print "file_name:    the name of the output file"
        print "============="
        exit(0)
    method_id = int(sys.argv[1])
    input_param = sys.argv[2]
    fname = sys.argv[3]
    if method_id == 1:
        scrapeNYT(input_param, fname)
    '''
    # scrape every popular news source
    for src in newspaper.popular_urls():
        bitcoin_news(src)
    '''
