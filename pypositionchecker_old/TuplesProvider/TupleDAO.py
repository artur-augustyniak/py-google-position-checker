#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Created on 18-02-2013

@author: artur
'''
import MySQLdb
import datetime
class TupleDAO(object):
    '''
    Model danych pozycji
    '''
    def __init__(self):
        '''
        Constructor mysql conn
        '''
        self.conn = MySQLdb.connect(host="localhost", user="", passwd="", db="", charset='utf8')
        c = self.conn.cursor()
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
            
    def getTuples(self):
        '''
            Getter Dataset do sprawdzenia
        '''
        return self.rows
    
    def saveResult(self, pos, key):
        '''
        Zapis rezultatu, automatycznie wybiera dzień. Update dla tego samego tylko jeżeli nowa pozycja lepsza
        '''
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO results VALUES(%s,%s,%s);", (key, pos, now))
        except MySQLdb.IntegrityError:
            c.execute("SELECT * FROM results WHERE `key`=%s AND `date`=%s;", (key, now))
            oldPos = c.fetchone()[1]
            if (pos!=0 and oldPos == 0)  or (oldPos > pos and pos !=0):
                c.execute("UPDATE results SET pos=%s WHERE `key`=%s AND `date` =%s;", (pos, key, now))
