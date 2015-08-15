
###
### crawler.py
###
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from webcorpus import WebCorpus
from getpage import real_get_page
from bs4 import BeautifulSoup, Comment
import requests
import json
import re

def get_all_links(page): # gets all external links on webpage
    soup = BeautifulSoup(page, "html.parser") 
    links = []
    for link in soup.find_all('a'):
	try:
	    url = link.get('href')
	    if url and url not in links and len(url) < 160:				
		if str(link.get('href')[:4]) == 'http' or str(link.get('href')[:5]) == 'https':
		    links.append(link.get('href'))
	except:
	    print "This is an error message! "+ str(link)
    return links
    

def get_all_words(page): # gets all visible text on webpage
    soup = BeautifulSoup(page, "html.parser")
    for element in soup(text=lambda text: isinstance(text, Comment)):
    	element.extract()
    soup = BeautifulSoup(str(soup), "html.parser")
    soup = soup.findAll(text=True)
    visible_texts = filter(visible, soup)
    words = []
    for x in visible_texts:
	for wrd in x.split():
	    valid = re.match('^[\w-]+$', wrd) is not None
	    if len(wrd) > 1 and valid and wrd.encode("UTF-8") not in words:
		words.append(str(wrd.encode("UTF-8")))
    return words
    


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title','link',',','.',' | ']:
        return False
    return True 
        
    
def crawl_web(seed,max_depth,crawled): # returns index, graph of inlinks"
    tocrawl = set(seed)
    next_depth = []
    depth = 0
    wcorpus = WebCorpus()
    last_url = None
    while tocrawl :             
        url = tocrawl.pop()
        if url not in crawled:  
            try:
                content = real_get_page(url)
                if content:
		    words = get_all_words(content)
		    if 'joe' in words or 'Joe' in words or 'joseph' in words or 'Joseph' in words:
			print url
			outlinks = get_all_links(content)
			for outlink in outlinks:
			    wcorpus.add_link(url,outlink)
			if depth >= max_depth:
			    outlinks = set(outlinks)
			    tocrawl.update(outlinks)
			    tolist = list(tocrawl)
			    write_tocrawl(tolist)
			    write_crawled(crawled)
			    return wcorpus
			soup = BeautifulSoup(content, "html.parser")
			try:
			    title = soup.title.string
			except:
			    title = ''
			try:
			    desc = str(soup.findAll(attrs={"name":"description"})[0]['content'].encode('utf-8'))
			except:
			    desc = ''
			
			for word in words:
			    wcorpus.add_word_occurrence(url,str(word.encode("UTF-8")),title,desc)
			tocrawl.update(outlinks)
			tolist = list(tocrawl)
			d = {'tocrawl':tolist}
			with open('tocrawl_json.json', 'w') as outfile:
			    json.dump(d, outfile)
			crawled.append(url)
			depth+=1
		    outlinks = get_all_links(content)
		    crawled.append(url)
		    tocrawl.update(outlinks)

            except Exception, e:
                print "ERROR "+str(e)

    print str(last_url) + ' ####  LAST URL NOTHING TO CRAWL ####'
    
    return wcorpus

def write_tocrawl(data):
    d = {'tocrawl':data}
    with open('tocrawl_json.json', 'w') as outfile:
        json.dump(d, outfile)

def write_crawled(data):
    d = {'crawled':data}
    with open('crawled_json.json', 'w') as outfile:
        json.dump(d, outfile)
    


    


