
###
### webcorpus.py
###
import json

class WebCorpus:
    def __init__(self):
        """
        Initializes a new, empty WebCorpus.
        """
        self._index = {}
        self._graph = {}
        self._ranks = None
        
    def __repr__(self):
        return str(self._index)
            

    def add_word_occurrence(self, url, keyword, title, desc):
        """
        Adds an occurrence of word on url to the corpus.
        """
        if url not in self._graph:
            self._graph[url] = []

        if keyword in self._index:
            if url not in self._index[keyword]:
                self._index[keyword].append([url,title,desc])
        else:
            self._index[keyword] = [[url,title,desc]]

    def add_link(self, source, sink):
        """
        If source is not a node in the corpus, adds source as a new node.
        If sink is not a node in the corpus, adds sink as a new node.
        Adds a link from source to sink to the corpus.
        """
        if source not in self._graph:
            self._graph[source] = [sink]
        else:
            self._graph[source].append(sink)
        self._ranks = None # invalidate ranks after each graph modification
	
    def add_info(self, url, soup):
	"""
	if url contains title/description, add to index
	"""
	try:
	    title = soup.title.string
	    print str(soup.title.string)
	    self._index
	except:
	    print 'no title'
    
    def _compute_ranks(self, d = 0.8, numloops = 100):
        """compute page ranks for the input web index.  d is the damping factor."""
        self._ranks = {}
        npages = len(self._graph)
        for url in self._graph:
            self._ranks[url] = 1.0 / npages    

        for i in range(0, numloops):
            newranks = {}
            for page in self._graph:
                newrank = (1 - d) / npages
                for node in self._graph:
                    if page in self._graph[node]:
                        newrank = newrank + d * (self._ranks[node] / len(self._graph[node]))
                    newranks[page] = newrank
            self._ranks = newranks

    def lookup(self, keyword):
        if keyword in self._index:
            return self._index[keyword]
        else:
            return None

    def page_rank(self, url):
        if not self._ranks:
            self._compute_ranks()
        if url not in self._ranks:
            return 0.0
        return self._ranks[url]
        
    def to_JSON(self):
        out = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.loads(out)


