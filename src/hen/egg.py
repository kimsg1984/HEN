#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

from HTMLParser import HTMLParser

default_style = {
    '#default'  : ('margin-top:0px', 'margin-bottom:0px', 'margin-left:0px', 'margin-right:0px'),
     'p'        : ('-qt-block-indent:0', 'text-indent:0px', '-qt-user-state:0', '-qt-user-state:0'),
     'li'       : ('-qt-block-indent:0', 'text-indent:0px', ),
     'ul'       : None,
     'ol'       : None,
}

def attrs_parser(attrs):
    result = ''
    def attr_parser(attr):
        attr = re.sub(r'(\ ?):(\ ?)', ':', attr)
        return attr


    for attr in attrs:
        id = attr[0]
        attr = attr_parser(attr[1])
    # attr = attr[1]
    result += '{}="{}"'.format(id, attr)

    return result

class HtmlFromFile(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.text = ''

	def handle_starttag(self, tag, attrs):
		if len(attrs) == 0:
			self.text += '<{}>'.format(tag)
		else:
			self.text += '<{} {}>'.format(tag, attrs_parser(attrs))

	def handle_endtag(self, tag):
		# print "Encountered an end tag :", tag
		self.text += "</" + tag + ">"

	def handle_data(self, data):
		self.text += data

class Egg(object):
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
            html = re.sub('<p>\n</p>', '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; -qt-user-state:0;"></p>', html)
            html = re.sub('<p>', '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; -qt-user-state:0;">', html)
            return html

        self.filename = filename
        # html = open(filename).read()
        # html = addTag(html)

        html = HtmlFromFile()
        html.feed(open(filename).read())
        text = open(filename).read()
        print(text)
        print(html.text)
        # self.html = unicode(html.text) # 불러올 때 unicode로인코딩
        self.html = unicode(text) # 불러올 때 unicode로인코딩
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
        # print(self.html)
        html.encode('utf-8')
        # html = removeTag(html) # 나중에 줄이고 살리는거 해보자.

        save_file.write('%s' %html)
        save_file.close()
