#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 15-07-2013
@author: Artur Augustyniask
'''
import urllib
from gScrap import GoogleSearch
from urlparse import urlparse
from Configuration import *
from Log import *

class PositionChecker(object):
    '''
    Sprawdza pozycję danego url-a dla podanej frazy
    '''
    def __init__(self, phrase, url, proxy, g_tld, lang, search_depth=20, google_res_per_page=10):
        if not isinstance(url, str):
            raise TypeError("expecting <str>")
        self.logger = Logger()
        self.sd = search_depth
        self.grpp = google_res_per_page
        self.outOfRange = search_depth * google_res_per_page
        self.position = self.outOfRange
        self.gs = GoogleSearch(phrase, proxy, g_tld, lang)
        self.gs.results_per_page = google_res_per_page
        self.sUrl = url
    
    def _canonizeDomain(self, domain):
        '''obcina subdomenę www'''
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
        
    
    def _isSearch(self, foundUrl):
        '''Sprawdza czy znaleziony url pokrywa się z szukanym'''
        searchUrl = urlparse(urllib.unquote_plus(self.sUrl))
        netLocMatch = False
        if Config.matchWww:
            netLocMatch = (foundUrl.netloc == searchUrl.netloc)
        else:
            netLocMatch = (self._canonizeDomain(foundUrl.netloc) == self._canonizeDomain(searchUrl.netloc)) 
        
        if Config.machCompleteUrls:
            return netLocMatch and (foundUrl.path == searchUrl.path) and (foundUrl.query == searchUrl.query)
        else:
            return netLocMatch  
            
                
    def analyzePosition(self):
        '''Obliczenie Pozycji wraz z modyfikacjami w Config'''
        mapsBackCounter = 0
        for i in range(0,self.sd):
            self.gs.page = i
            results = self.gs.get_results()
            j = 1
            for res in results:
                foundUrl = urlparse(urllib.unquote_plus(res.url))
                if Config.verbose:
                    self.logger.logOnConsole('Badany url: '+res.url)
                if self._isSearch(foundUrl):
                    position = i*self.grpp+j
                    '''Jeśli trafienie jest poza mapkami odliczmy ilośc mapek od wyniku, domeny ignorowane nie będa odliczone dwa razy'''
                    if res.desc and Config.enableMapsBoost:
                        position -= mapsBackCounter 
                    return self._seoBounce(position)
                '''Zapamiętujemy ilośc mapek i wyników generowanych przez google'''
                if not res.desc and not (foundUrl.netloc in Config.ommitDomains) and Config.enableMapsBoost:
                    mapsBackCounter+=1
                '''Jeśli nie na liście pomijanych domen doliczamy do pozycji'''
                if not foundUrl.netloc in Config.ommitDomains:
                    j+=1        
        return self.outOfRange
    
    def _seoBounce(self, posNum):
        '''Podbicie Krytycznych pozycji wg listy w Config'''
        if posNum in  Config.bounceOneUpOn:
            posNum -= 1
        return posNum