#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

"""PyQt4 port of the richtext/syntaxhighlighter example from Qt v4.x"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import highlighter

generateFormat = highlighter.generateFormat

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

		self.highlighter = highlighter.Highlighter(self.editor.document())

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