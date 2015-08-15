"""
Change the code here to use the new WebCorpus type.
"""

###
### search.py
###

def lookup(windex, keyword):
    if keyword in windex.index:
        return windex.index[keyword]
    else:
        return None

def lucky_search(wcorpus, keyword):
    pages = wcorpus.lookup(keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        # Note: you should not use the _ranks attribute: the _ indicates it is private to the
        #    WebCorpus object.
        if wcorpus.page_rank(candidate) > wcorpus.page_rank(best_page):
                best_page = candidate
    return best_page

def quicksort_pages(pages, wcorpus):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = wcorpus.page_rank(pages[0])
        worse = []
        better = []
        for page in pages[1:]:
            if wcorpus.page_rank(page) <= pivot and page not in worse:
                worse.append(page)
            else:
                better.append(page)
        return quicksort_pages(better, wcorpus) + [pages] + quicksort_pages(worse, wcorpus)
            
def ordered_search(wcorpus, keyword):
    pages = wcorpus.lookup(keyword)
    if pages:
        
        return quicksort_pages(pages, wcorpus)
    else:
        print 'no pages'
        
def easy_search(wcorpus, keyword):
    pages = wcorpus.lookup(keyword)
    if pages:
        
        print pages
    else:
        print 'no pages'
