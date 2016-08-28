#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import smtplib
os.chdir("/home/ithld/bots/pypositionchecker_old/googlecrawler")
sys.path.append("../")
from datetime import datetime
from TuplesProvider import TupleDAO
from pyRandomizer import Randomizer
from pyBrowser import Browser, BrowserError
from logger import Logger
from SeoProcessor import TupleProcessor
from gScrap import SearchError, Error

starttime = unicode(datetime.now())
sender = ''
recievers = ['']
message = """From:
To:
Subject: Start Round
Run at """+starttime.encode("utf-8")+""" started.
"""
try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, recievers, message)
    print "Sending initial Msg"
except SMTPException:
    print "Can't send error initial - SMTP error"

idleRange = 2
randomizer = Randomizer(idleRange)
tuples = TupleDAO()
for tup in tuples.getTuples():
    exact_url = tup[1]    
    phrase = tup[2]
    google_lng = tup[3] 
    key_id = tup[4]
    try:
        pos = TupleProcessor(randomizer, google_lng, phrase, exact_url, idleRange, 5, 10)   
        tuples.saveResult(pos.getCurrPos(), key_id) 
        print str(pos.getCurrPos()) + " " +  phrase + " "+ exact_url
        randomizer.randomSleep()     
    except  (SearchError, BrowserError):
        tuples.rows.append(tup);
        print "Browser error for phrase ["+phrase+"] rebuilding queue"
        continue

endtime = unicode(datetime.now())
message = """From:
To:
Subject: Finish Round
Round started at """+starttime.encode("utf-8")+""" finished at """+endtime.encode("utf-8")+""".
"""
try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, recievers, message)
    print "Sending finish Msg"
except SMTPException:
    print "Can't send error finish - SMTP error"
