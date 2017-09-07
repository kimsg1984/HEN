#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class Note(object):
    """
    노트 클래스.
    """
    def __init__(self, filename = None):
        self.filename = ''
        self.title = ''
        self.html = ''
        if filename: self.setFile(filename)

    def setFile(self, filename):
        def addTag(html):
            html = re.sub('<p>\n</p>', '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; -qt-user-state:0;">', html)
            html = re.sub('<p>', '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; -qt-user-state:0;">', html)
            return html
        self.filename = filename
        html = open(filename).read()
        # html = addTag(html)
        self.html = unicode(html) # 불러올 때 unicode로인코딩
        self.title = ''

    def setHtml(self, html):
        self.html = html

    def saveFile(self):
        def removeTag(html):
            html = re.sub(r'<!(.+?)>\n', '', html)
            html = re.sub(r'\n', '<br />', html)
            # html = re.sub(r'<head>(.+?)</head>', '', html)
            html = re.sub(r'<p style=(.+?)>', '<p>', html)
            html = re.sub(r'<br />', '\n', html)
            return html
            
        save_file = open(self.filename, 'w')
        html = '%s' %self.html
        html.encode('utf-8')
        # html = removeTag(html)

        save_file.write('%s' %html)
        save_file.close()