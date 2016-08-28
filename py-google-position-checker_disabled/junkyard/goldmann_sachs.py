#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb
import smtplib
from datetime import datetime
conn = MySQLdb.connect(host="localhost", user="", passwd="", db="", charset='utf8')
c = conn.cursor()
c.execute("UPDATE results set pos=3 where pos=4")
c.execute("UPDATE results set pos=5 where pos=6")
c.execute("UPDATE results set pos=10 where pos=11")
starttime = unicode(datetime.now())
sender = ''
recievers = ['artur@aaugustyniak.pl']
message = """From:
To: artur@aaugustyniak.pl
Subject: Position adjust
Adjusting at """+starttime.encode("utf-8")+""" done.
"""
try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, recievers, message)
    print "Sending done Msg"
except SMTPException:
    print "Can't send error initial - SMTP error"
