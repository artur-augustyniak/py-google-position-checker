#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Created on 18-02-2013

@author: artur
'''
import MySQLdb
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from Log import *
class ResultsDAO(object):
    '''
    Model danych pozycji, dokonuje automatycznej archiwizacji
    '''
    def __init__(self):
        '''
        Constructor mysql conn
        '''
        try:
	    self.conn = MySQLdb.connect(host="localhost", user="l", passwd="", db="", charset='utf8')
            #self.conn = MySQLdb.connect(host="localhost", user="root", passwd="5428slony", db="mde_panelutf8", charset='utf8')
        except MySQLdb.OperationalError:
             l = Logger()
             l.sendEmail('Problem z połączeniem z bazą danych')
             exit()
        c = self.conn.cursor()
        self._checkArchivisation(c)
        c.execute("SELECT s.id, s.url, k.keyword, s.google, k.id_key FROM sites s INNER JOIN keywords k ON s.id = k.site_id WHERE s.active = 1;")
        self.rows = []
        for row in c.fetchall():
            tmp_row = []
            tmp_row.append(row[0])
            tmp_row.append(row[1].strip('http://"').encode("utf-8"))
            tmp_row.append(row[2].encode("utf-8"))
            tmp_row.append(row[3])
            tmp_row.append(row[4]) 
            self.rows.append(tmp_row)
            
    def _checkArchivisation(self, c):
        '''Utrzymuje w results tylko dany miesiąc'''
        targetDate =  date.today() + relativedelta( months = -1 )
        targetYear = targetDate.year
        targetMonth =  targetDate.strftime("%m")
        try:
            c.execute("INSERT INTO archive SELECT * FROM results WHERE year( date ) = %s AND month( date ) = %s;", (targetYear, targetMonth))
        except MySQLdb.IntegrityError:
            pass
        try:
            c.execute("DELETE FROM results WHERE year( date ) = %s AND month( date ) = %s;", (targetYear, targetMonth))
        except MySQLdb.IntegrityError:
            pass

              
    def getTuples(self):
        '''
            Getter Dataset do sprawdzenia
        '''
        return self.rows
    
    def saveResult(self, pos, key):
        '''
        Zapis rezultatu, automatycznie wybiera dzień. Update dla tego samego tylko jeżeli nowa pozycja lepsza
        '''
        now = datetime.now()
        now = now.strftime("%Y-%m-%d")
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO results VALUES(%s,%s,%s);", (key, pos, now))
        except MySQLdb.IntegrityError:
            c.execute("SELECT * FROM results WHERE `key`=%s AND `date`=%s;", (key, now))
            oldPos = c.fetchone()[1]
            if (pos!=0 and oldPos == 0)  or (oldPos > pos and pos !=0):
                c.execute("UPDATE results SET pos=%s WHERE `key`=%s AND `date` =%s;", (pos, key, now))
