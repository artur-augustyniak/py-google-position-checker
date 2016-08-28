#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 18-02-2013

@author: artur
''' 
from gScrap import GoogleSearch
from urlparse import urlparse
class TupleProcessor(object):
    '''
    classdocs
    '''

    def __init__(self,randomizer, google_lng, phrase, exact_url, max_idle_time=5, search_depth=50, google_res_per_page=10):
        '''
        Constructor
        ''' 
	lang = "pl"
	if(google_lng !="pl"):
		lang = "en"
        gs = GoogleSearch(randomizer, phrase, lang, google_lng, None)
        results = []
        self.output = 0;
        self.res_per_page = google_res_per_page
        self.search_depth = search_depth
        try:
            for i in range(search_depth):
                gs.page = i
                results = gs.get_results()
               	results = filter(self.isOrganic, results)
                onPage = 1;
                for res in results:
                    safe_res_url = urlparse(res.url)                    
                    if exact_url in safe_res_url.netloc:
                        self.output = i * google_res_per_page +onPage
                        raise GetOutOfLoop
                    onPage +=1
        except GetOutOfLoop:
            pass
    
    def isOrganic(self, res):
        try:
            if len(res.desc) > 0:
                return True
            else:
                return False
        except TypeError:
            return False
    
            
    def getCurrPos(self):
        if self.output == 0:
            #poza zasięgiem
            return self.res_per_page * self.search_depth +1
        else:
            return self.output
                
class GetOutOfLoop( Exception ):
    pass
            
            
