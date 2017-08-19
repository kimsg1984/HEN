#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
reload(sys)
import signal

# from PyQt4 import QtCore
# from PyQt4 import QtGui

from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
	 from highlighter import Highlighter
except ImportError, err:
 	sys.stderr.write("Error: %s%s" % (str(err), os.linesep))
 	sys.exit(1)

class NoteEditor(QDialog):
	def __init__(self, parent=None):
		super(NoteEditor, self).__init__(parent)
		self.editor = QTextEdit()
		self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.editor.setAcceptRichText(False)
		# self.editor.setTextInteractionFlags(Qt.LinksAccessibleByMouse) # 링크로 접속 허용??
		layout = QVBoxLayout() # appear virtically
		layout.setMargin(0)
		layout.addWidget(self.editor)
		self.menuBar = QMenuBar(self)
		layout.setMenuBar(self.menuBar)
		self.setupMenu()
		self.setLayout(layout)


		self.highlight = Highlighter(self.editor.document())
		self.highlight.addKeyword('class')
		self.resize(500, 500)

		self.mouse_under_text = ''

	def setupMenu(self):
		fileMenu = QMenu("&File", self)
		self.menuBar.addMenu(fileMenu)

	def eventFilter(self, source, event):
		if event.type() == QEvent.MouseMove:
			if event.buttons() == Qt.NoButton:				
				pos = event.pos()
				# print(pos)
				virtual_cursor =  self.editor.cursorForPosition(event.pos()) # 설렉션 잡을 때 마다 생성해줘야 함.
				virtual_cursor.select(QTextCursor.WordUnderCursor)
				self.virtual_cursor = virtual_cursor
				text = virtual_cursor.selectedText()
				if len(text) > 1:
					if self.mouse_under_text != text:
						sentence = 'selectedText: %s' %text
						sentence = sentence.encode('utf-8')
						print('%s' %(sentence))
						self.mouse_under_text = text
						if virtual_cursor.charFormat().isAnchor():
							print(virtual_cursor.charFormat().anchorHref())
							self.editor.viewport().setCursor(QCursor(Qt.PointingHandCursor))
						else:
							self.editor.viewport().setCursor(QCursor(Qt.IBeamCursor))
					else:
						self.editor.viewport().setCursor(QCursor(Qt.IBeamCursor))
				else:
					self.mouse_under_text =''
					pass # do other stuff
	
		return self.editor.eventFilter(self, event)

