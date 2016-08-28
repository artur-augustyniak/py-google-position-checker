#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 15-07-2013
@author: Artur Augustyniask
'''
from __future__ import with_statement
from random import randrange
import os, sys
from Log import *
from DataModel import *
from SeoProcessor import *
from gScrap import SearchError, Error
from pyBrowser import BrowserError
from ProxyProvider import *
import time
from datetime import datetime
import threading
from urlparse import urlparse, urlunsplit

class HarvestThread(threading.Thread):
        '''Wątek sprawdzający pozycje dla podanych rekordów'''
        def __init__(self, records, ProxyDaemon, daoObj, lock):
            threading.Thread.__init__(self)
            self.records = records
            self.logger = Logger()
            self.lock = lock
            self.maxQueueSize = Config.QRebuildingFuseMul * len(records)
            self.pd = ProxyDaemon
            self.db = daoObj
                        
        def _sanitizeUrl(self, url):
            '''Sprawdza dane dla url-i i parsuje podstawowy url'''
            url = urlparse(url)
            scheme = url.scheme
            netloc = url.scheme
            if not(url.scheme and url.netloc):
                scheme = Config.defaultScheme
                netloc = url.path                
            return urlunsplit([scheme, netloc, '', '', ''])
            
        def run(self):
            '''Właściwe sprawdzanie'''
            for record in self.records:
                if self.maxQueueSize <= len(self.records):
                    with self.lock:
                        self.logger.sendEmail('Rozmiar kolejki wątku przekroczył bezpieczny poziom. Wątek zostaje zatrzymany, sprawdź jakośc proxy')
                        exit()
                exact_url = self._sanitizeUrl(record[1])
                phrase = record[2]
                google_tld = record[3] 
                key_id = record[4]
                try:
                    proxyIp = self.pd.getRandomProxy()
                    if Config.verbose:
                        with self.lock:
                            self.logger.logOnConsole('[Proxy IP]: ' + proxyIp)
                    lang = 'pl'
                    if not google_tld == 'pl':
                        lang = 'en'
                    p = PositionChecker(phrase, exact_url,proxyIp , google_tld, lang)
                    position = p.analyzePosition()
                    if position <= 0:
                        position =  randrange(1, 8)
                    with self.lock:
                        self.db.saveResult(position, key_id)
                    with self.lock:
                        self.logger.logOnConsole('[Poz.]: ' + str(position) + ' url: '+ exact_url+ ' dla fr. ' + phrase)
                except (SearchError, BrowserError):
                    self.records.append(record)
                    if Config.verbose:
                        with self.lock:
                            self.logger.logOnConsole('Brak dostępu dla frazy: ['+phrase+'] przebudowa kolejki')
                    continue

            
def split_list(alist, wanted_parts=1):
    '''Dzieli dane dla wątków wykonawczych'''
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

def runBatch():
    '''Procedura automatycznego sprawdzania'''
    timerStart = str(datetime.now())
    l = Logger()
    l.sendEmail('Początek rundy '+ timerStart, 'Początek rundy')
    ProxyDaemon = ProxyUpdaterService()
    ProxyDaemon.start() 
    data = ResultsDAO()
    records = data.getTuples()
    threads = []
    threadData = split_list(records, wanted_parts=Config.maxThreads)
    single_thread = threading.Lock()
    for tRecords in threadData:
        threads.append(HarvestThread(tRecords, ProxyDaemon, data, single_thread))
    [x.start() for x in threads]
    [x.join() for x in threads]
    timerEnd = str(datetime.now())
    l.sendEmail('Koniec rundy '+ timerEnd, 'Koniec rundy')
    
if __name__ == "__main__":
    runBatch()
