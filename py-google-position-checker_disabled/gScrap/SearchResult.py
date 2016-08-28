#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 13-02-2013

@author: artur
'''
class SearchResult:
    def __init__(self, title, url, desc, gurl):
        self.title = title
        self.url = url
        self.desc = desc
        self.gurl = gurl

    def __str__(self):
        return 'Google Search Result: "%s"' % self.title
