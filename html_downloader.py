# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:26:40 2017

@author: Frank
"""

import urllib.request

class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            return None

        return response.read()
        # response = response.decode('utf-8')