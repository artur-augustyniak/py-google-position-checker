#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Created on 28-02-2013

@author: artur
'''
from datetime import datetime

class Logger(object):
    '''
    classdocs
    '''

    def __init__(self, filepath, message):
        '''
        Constructor
        '''
        time = unicode(datetime.now())
        message = message.decode("utf-8")
        
        with open(filepath, "a") as logfile:
            message = "["+time.encode("utf-8")+"]-"+message.encode("utf-8")+"\n"
            logfile.write(message)    
        
        