#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Created on 18-02-2013

@author: artur
'''
import random
import time
import smtplib
from pyBrowser import Browser, BrowserError
from datetime import datetime
from IPy import IP

class Randomizer(object):
    '''
    classdocs
    '''
    def __init__(self, max_idle_time = 2):
        '''
        Constructor
        '''
        self.max_idle_time = max_idle_time
	browser = Browser()
	try:
	    print "getting proxy"
	    #rawProxies = browser.get_page("http://www.proxymarket.pl/api/get/ae6f81cd2414932082061ab9161ed560/")
            rawProxies = browser.get_page("http://www.proxymarket.pl/api/get/38ed4fbd878dfd8b65c3aa28597d373cc44f7159")
	    self.PROXIES = rawProxies.split()
            for ip in self.PROXIES:
		IP(ip[:ip.rfind(':')])
	except ValueError:
	    time = unicode(datetime.now())
	    sender = ''
	    recievers = ['']
	    message = """From:
To:
Subject: Proxy Error
Run at """+time.encode("utf-8")+""" failed - initial proxylist fetching error
"""
	    try:
	        smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, recievers, message)
		print "Sending error Msg"
	    except SMTPException:
	        print "Can't send error Msg - SMTP error"
	    print "Can't fetch proxy list"
	    exit()
        
    def getIntTo(self, rangeMax):
        return random.randint(0, rangeMax)
    
    def randomSleep(self):
        idle_time = self.getIntTo(self.max_idle_time)
        time.sleep(idle_time)
        return idle_time
    
    def getRandomProxy(self):
        return random.choice(self.PROXIES)
    
        

