#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

"""PyQt4 port of the richtext/syntaxhighlighter example from Qt v4.x"""

import logging
from PyQt4.QtGui import *
from PyQt4.QtCore import *

log = logging.getLogger(__name__)

def generateFormat(color=None, size=None, underline=False):
	keywordFormat = QTextCharFormat()
	if color : keywordFormat.setForeground(color) # QT.$color
	if size 	: keywordFormat.setFontPointSize(size)
	if underline: keywordFormat.setFontUnderline(True)
	return keywordFormat

class Highlighter(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super(Highlighter, self).__init__(parent)

		self.keywordFormat = generateFormat(color = Qt.blue, underline = True)
		self.keywordFormat.setAnchor(True)

		self.highlightingRules = []
		self.highlight_information = {} # $block_number : [[$index_start, $index_end, '$index_type', '$link_to'], ...]

	def addKeyword(self, keyword):
		self.highlightingRules.append((QRegExp("\\b%s\\b" %keyword, Qt.CaseInsensitive), self.keywordFormat))

	def highlightBlock(self, text):
		def popHighlightInformation(block_number, info_list):
			if block_number in self.highlight_information:
				self.highlight_information[block_number].append(info_list)
			else:
				self.highlight_information[block_number] = [info_list]

		block_number = self.currentBlock().blockNumber()
		if block_number == 0: #title
			self.setFormat(0, len(text), generateFormat(color = Qt.blue, size = 20, underline = True))

		else:
			for pattern, format in self.highlightingRules:
				expression = QRegExp(pattern)
				index = expression.indexIn(text)
				while index >= 0:
					length = expression.matchedLength()
					link_text = '{}'.format(text[index:index + length])
					popHighlightInformation(block_number, [index, index + length, 'inter_link', link_text])
					log.debug('{},{},{}'.format(block_number, index, length, link_text))
					format.setAnchorHref(link_text)
					self.setFormat(index, length, format)
					index = expression.indexIn(text, index + length)
			self.setCurrentBlockState(0)