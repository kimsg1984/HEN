#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

"""PyQt4 port of the richtext/syntaxhighlighter example from Qt v4.x"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


def generateFormat(color=None, size=None, underline=False):
	keywordFormat = QTextCharFormat()
	if color : keywordFormat.setForeground(color) # QT.$color
	if size 	: keywordFormat.setFontPointSize(size)
	if underline: keywordFormat.setFontUnderline(True)
	return keywordFormat

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupEditor()

		self.setCentralWidget(self.editor)
		self.setWindowTitle("Syntax Highlighter")

	def setupEditor(self):
		font = QFont()
		font.setFamily('Courier')
		font.setFixedPitch(True)
		font.setPointSize(10)

		self.editor = QTextEdit()
		self.editor.setFont(font)

		self.highlighter = Highlighter(self.editor.document())

class Highlighter(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super(Highlighter, self).__init__(parent)

		self.keywordFormat = generateFormat(color = Qt.blue, underline = True)
		self.keywordFormat.setAnchor(True)

		self.highlightingRules = []

	def addKeyword(self, keyword):
		self.highlightingRules.append((QRegExp("\\b%s\\b" %keyword, Qt.CaseInsensitive), self.keywordFormat))

	def highlightBlock(self, text):
		if self.currentBlock().blockNumber() == 0: #title
			self.setFormat(0, len(text), generateFormat(color = Qt.blue, size = 20, underline = True))

		else:
			for pattern, format in self.highlightingRules:
				expression = QRegExp(pattern)
				index = expression.indexIn(text)
				while index >= 0:
					length = expression.matchedLength()
					self.setFormat(index, length, format)
					index = expression.indexIn(text, index + length)
			self.setCurrentBlockState(0)
		# startIndex = 0

class Main():
	def __init__(self):
		import sys
		self.app = QApplication(sys.argv)
		self.window = MainWindow()
		self.window.resize(640, 512)
		self.window.highlighter.addKeyword('class')
		self.window.editor.textCursor().insertText('class')
		self.window.show()

	def exec_(self):
		self.app.exec_()

if __name__ == '__main__':
	m = Main()
	m.exec_()

# if __name__ == '__main__':