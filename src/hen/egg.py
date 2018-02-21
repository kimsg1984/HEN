#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint

import HtmlToNotefile
import IO

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

		self.filename = filename
		text = open(filename).read()
		# self.html = unicode(html.text) # 불러올 때 unicode로인코딩
		self.html = unicode(text) # 불러올 때 unicode로인코딩
		self.title = ''

	def setHtml(self, html):
		self.html = html

	def saveFile(self):

		save_file = open(self.filename, 'w')
		html = '%s' %self.html
		html.encode('utf-8')
		HtmlToNoteFile = HtmlToNotefile.HtmlToNoteFileFormat(IO.encode_utf(html))
		print(HtmlToNoteFile.listToMarkup())

		save_file.write('%s' %html)
		save_file.close()
