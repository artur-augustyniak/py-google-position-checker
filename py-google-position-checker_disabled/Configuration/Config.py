#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 15-07-2013
@author: Artur Augustyniask
'''
class Config:
    
    '''Ustawienia pobierania proxy'''
    minSecondsProxyInterval = 50
    spanSecondsProxyInterval = 20
    proxyApiUrl = 'http://ithld.linuxpl.info/proxy.php?key='
    constantInitialProxies = ['103.4.156.42:8888',
                              '118.101.184.163:8118',
                              '122.200.56.52:80',
                              '125.166.231.85:3128',
                              '171.97.163.235:3128',
                              '176.205.167.84:8118',
                              '180.253.239.192:3128',
                              '181.64.87.37:3128',
                              '183.182.84.169:3128']
    
    '''Parametry Środowiska'''
    debug= False
    maxThreads = 10
    verbose = False
    defaultScheme = 'http'
    '''Określa ile razy może być większa przebudowana kolejka od datasetu'''
    QRebuildingFuseMul = 10
    
    '''Parametry Crawlera'''
    bounceOneUpOn = [4, 6, 11]
    ommitDomains = ['www.zumi.pl', 'plus.google.com', 'webcache.googleusercontent.com', 'maps.google.pl']
    enableMapsBoost = True
    '''Uznaje za znaleziony jeżeli domena się zgadza'''
    machCompleteUrls = False
    '''Czy traktować www jako subdomenę'''
    matchWww = False
    
    '''Parametry Mailingu'''
    defaultMailSubj = 'Info'
    defaultDiagnosticsRcps = ['biuro@itholding.pl']
    mailerConfig = {
                    'sender':'',
                    'smtp':'',
                    'port':587,
                    'user': '',
                    'pass' : ''
                    }
