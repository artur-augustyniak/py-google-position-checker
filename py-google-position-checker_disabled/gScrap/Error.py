#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 13-02-2013

@author: artur
'''

class SearchError(Exception):
    """
    Base class for Google Search exceptions.
    """
    pass

class ParseError(SearchError):
    """
    Parse error in Google results.
    self.msg attribute contains explanation why parsing failed
    self.tag attribute contains BeautifulSoup object with the most relevant tag that failed to parse
    Thrown only in debug mode
    """
     
    def __init__(self, msg, tag):
        self.msg = msg
        self.tag = tag

    def __str__(self):
        return self.msg

    def html(self):
        return self.tag.prettify()
