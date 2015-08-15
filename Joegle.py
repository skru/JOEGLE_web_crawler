
from crawler import crawl_web
from search import lucky_search, ordered_search, easy_search
from webcorpus import WebCorpus
import json
import requests


######################################################
# COMMENT THIS SECTION OUT AFTER RUNNING THE FIRST TIME
# try and think of a page that has shit loads of external links
seed = ['http://www.dmoz.org/']

d = {'tocrawl':seed}
with open('tocrawl_json.json', 'w') as outfile:
    json.dump(d, outfile)
    
d = {'crawled':[]}
with open('crawled_json.json', 'w') as outfile:
    json.dump(d, outfile)
######################################################



count = 0
maxc = 50000
while count < maxc:

    print 'crawling web'
    data_file = open('tocrawl_json.json', 'r')
    data = json.load(data_file)

    url = data['tocrawl']
    crawled_data_file = open('crawled_json.json', 'r')
    crawled_data = json.load(crawled_data_file)
    crawled = crawled_data['crawled']
    pages_crawled = len(crawled)
    print pages_crawled
    

    corpus = crawl_web(url,3,crawled)

    print 'crawled'




    ### After the crawler has done its shizzle it sends the data as JSON to my site 
    ### feel free to uncomment but i don't know how much data the server can recieve at once, 
    ### also it might be too much for Mysql to handle at once' 
    
    #json_corpus = corpus.to_JSON()

    #print 'saving corpus to server'
     
    #url = "http://www.josephmohan.co.uk/crawler/json_reciever"
    #datatosend = json_corpus

    #headers = {'content-type': 'application/json'}
    #r = requests.post(url, data=json.dumps(json_corpus), headers=headers, timeout=60*10)

    #jsoner.put(json_corpus,"json_response.json")
   
    
    count+=1
    




