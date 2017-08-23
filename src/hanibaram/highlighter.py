#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

"""PyQt4 port of the richtext/syntaxhighlighter example from Qt v4.x"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

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

		self.keywordFormat = QTextCharFormat()
		self.keywordFormat.setForeground(Qt.blue)
		self.keywordFormat.setFontUnderline(True)
		self.keywordFormat.setAnchor(True)
		self.keywordFormat.setAnchorHref(QString('https://google.com'))

		# keywordFormat.setAnchorNames(QStringList('class'))
		self.highlightingRules = []

	def addKeyword(self, keyword):
		self.highlightingRules.append((QRegExp("\\b%s\\b" %keyword, Qt.CaseInsensitive), self.keywordFormat))
		# self.highlightingRules.append((QRegExp("\\b%s\\b" %keyword), self.keywordFormat))

	def highlightBlock(self, text):
		print_dir = dir(self); print_dir.sort();print('dir: self'); print(',\n'.join(print_dir)); del print_dir
		print(self.parent().toHtml())

		for pattern, format in self.highlightingRules:
			expression = QRegExp(pattern)
			index = expression.indexIn(text)
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)
		self.setCurrentBlockState(0)

		startIndex = 0

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