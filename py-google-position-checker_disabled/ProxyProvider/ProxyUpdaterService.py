#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 18-07-2013
@author: Artur Augustyniask
'''
from __future__ import with_statement
import threading
import time
from Configuration import *
from pyBrowser import Browser, BrowserError
from Log import *
from IPy import IP
import random



class ProxyUpdaterService(threading.Thread):
    
        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
            self.proxies = Config.constantInitialProxies
            self.browser = Browser()
            self.logger = Logger()
            
            
            
        def getRandomProxy(self):
            p = None
            try:
                p = random.choice(self.proxies)
            except IndexError:
                pass
            return p 

        def run(self):         
            while True:
                time.sleep(random.randint(Config.minSecondsProxyInterval, Config.minSecondsProxyInterval+ Config.spanSecondsProxyInterval))
                succ = False
                try:
                    rawProxies =  self.browser.get_page(Config.proxyApiUrl)
                    rawProxies = rawProxies.split()
                    for ip in rawProxies:
                        IP(ip[:ip.rfind(':')])
                    succ = True
                except (ValueError, BrowserError):
                    self.logger.logOnConsole('Błąd pobierania proxy')
                    pass
                if succ:
                    self.logger.logOnConsole('Update Proxy')
                    #self.proxies = Config.constantInitialProxies+rawProxies
                    self.proxies = Config.constantInitialProxies+rawProxies