import urllib2
from xml.dom.minidom import parseString
import requests

def get_google_new_results( term, count ):
    results = []
    #obj = parseString( urllib2.urlopen('https://news.google.com/news?q=%s&output=rss' % term).read() )
    # req = urllib2.Request('https://news.google.com/news?q=%s&output=rss' % term, headers={'User-Agent': 'Mozilla/5.0'})
    #req = urllib2.Request('http://www.google.com/search?q=%s&hl=en&gl=us&authuser=0&source=lnt&tbm=nws' % term, headers={'User-Agent': 'Mozilla/5.0'})
    # obj = parseString(urllib2.urlopen(req).read())
    # url = 'http://www.google.com/search'
    # params = {'q':term, 'hl':'en', 'gl':'us', 'authuser':0, 'source':'lnt', 'tbm':'nws', 'output':'rss'}
    url = 'https://news.google.com/news'
    params = {'q':term, 'output':'rss'}
    r = requests.get(url, params=params)
    # print parseString(r.raw.read())
    for item in r.headers.iteritems():
        print item
    # r.encoding = 'utf-8'
    # print r.encoding
    # print parseString(r.text)
    # elements = obj.getElementsByTagName('title')[2:] # To get rid of unwanted title elements in XML doc    
    # links = obj.getElementsByTagName('link')[2:]
    # #print links
    # for element in elements[:count]:
    #     headline =  element.childNodes[0].data
    #     for link in links:
    #         url = link.childNodes[0].data.split('=')[-1]
    #     newssearch = headline + ' -> ' + url
    #     results.append( newssearch )

    # return results

get_google_new_results( 'apple', 5 )
# items = get_google_new_results( 'apple', 5 )
# for i,e in enumerate(items):
#     print '%d: %s' % (i+1,e,)
