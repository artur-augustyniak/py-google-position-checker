#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Created on 28-02-2013

@author: Artur Augustyniak
'''
import smtplib
from Configuration import *
from datetime import datetime


class Logger(object):
    '''
    Logowanie na konsolę oraz email
    '''
  
    def logOnConsole(self, msg):
        if Config.verbose:
            print unicode(datetime.now())+' - '+msg.decode('utf-8')
                    
    def sendEmail(self, msg, subj=None, rcps=None):
        if Config.debug:
            self.logOnConsole(msg)
            return
        try:  
            smtpserver = smtplib.SMTP(Config.mailerConfig['smtp'],Config.mailerConfig['port'])
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(Config.mailerConfig['user'], Config.mailerConfig['pass'])
            if not subj:
                subj= Config.defaultMailSubj
            header = 'From: ' + Config.mailerConfig['sender'] + '\n'+'Content-type: text/plain; charset=utf-8 \n' + 'Subject:'+subj+'\n'
            msg = header +'\n'+msg
            if not rcps:
                rcps = Config.defaultDiagnosticsRcps
            smtpserver.sendmail(Config.mailerConfig['sender'], rcps, msg)
            smtpserver.close()
        except SMTPException:
            self.logOnConsole("Can't send error initial - SMTP error")
