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
import re
import sys
reload(sys)
import logging
sys.setdefaultencoding('utf-8')
# sys.setrecursionlimit(10000)

log = logging.getLogger(__name__)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
	from highlighter import Highlighter
	from note import Note
	from reference import event_type
	from reference import font_size
	from reference import key_type
	from qtextedit import TextEdit

except ImportError, err:
	log.warning("Error: %s%s" % (str(err), os.linesep))
	sys.exit(1)

def keyCode(code): return key_type[code] if key_type.has_key(code) else code

class NoteEditor(QDialog):
	def __init__(self, parent=None):
		super(NoteEditor, self).__init__(parent)
		# self.editor = TextEdit()
		self.editor = TextEdit()
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

		# self.highlight = Highlighter(self.editor.document())
		# self.highlight.addKeyword('class')
		# self.highlight.addKeyword('clas.cs')

		self.resize(700, 700)
		self.mouse_under_text = ''
		self.is_editing_title = False
		self.__declineInstance()
		self.note = Note()

	def __declineInstance(self):
		self.color_white = '#ffffff'
		self.color_highlight = '#ffff00'

	def isTitle(self):
		return True if self.editor.textCursor().blockNumber() == 0 else False

	def setupMenu(self):

		fileMenu = QMenu("&File", self)
		self.menuBar.addMenu(fileMenu)
		fileMenu.addAction("&Save...", 		self.saveFile, 			"Ctrl+S")

		editMenu = QMenu("&Edit", 	self)
		styleMenu = QMenu("S&tyle", self)
		sizeMenu = QMenu("&Size", self)
		indentMenu = QMenu("&Indent", self)
		self.menuBar.addMenu(editMenu)
		# self.menuBar.addMenu(styleMenu)
		# self.menuBar.addMenu(sizeMenu)
		# self.menuBar.addMenu(indentMenu)
		editMenu.addAction("&Bord", 		self.textBold, 			"Ctrl+B")
		editMenu.addAction("&Italic", 		self.textItalic, 		"Ctrl+I")
		editMenu.addAction("&Highlight", 	self.textHighlight, 	"Ctrl+H")
		editMenu.addAction("&Strikethrough", self.textStrikethrough, "Ctrl+T")
		editMenu.addAction("&Underline", 	self.textUnderline, 	"Ctrl+U")
		editMenu.addSeparator()
		editMenu.addAction("S&mall", 		self.textSizeSmall, 	"Ctrl+1")
		editMenu.addAction("&Normal", 		self.textSizeNormal, 	"Ctrl+2")
		editMenu.addAction("&Large", 		self.textSizeLarge, 	"Ctrl+3")
		editMenu.addAction("&X-Large", 		self.textSizeXLarge, 	"Ctrl+4")
		editMenu.addSeparator()
		editMenu.addAction("Indent", 		self.textIndent, 		"Alt+Right")
		editMenu.addAction("Dedent", 		self.textDedent, 		"Alt+Left")
		editMenu.addAction("Number/Bullet", 	self.textNumOrBullet, "Alt+N")

	def setNote(self, note):
		self.note = note
		html = note.html
		self.editor.setHtml(html)
		c = self.editor.textCursor()
		# 타이틀이나 여는 시간등도 설정할 것.

	## MenuBar Function ##
	# File Menu #
	def saveFile(self):
		html = self.editor.toHtml()
		self.note.setHtml(self.editor.toHtml())
		self.note.saveFile()

	# Edit Menu #
	def textBold(self):
		if self.isTitle(): return

		if self.editor.fontWeight() == QFont.Bold:
			self.editor.setFontWeight(QFont.Normal)
		else:
			self.editor.setFontWeight(QFont.Bold)

	def textItalic(self):
		if self.isTitle(): return
		state = self.editor.fontItalic()
		self.editor.setFontItalic(not state)

	def textHighlight(self):
		if self.isTitle(): return
		color = self.editor.textBackgroundColor()
		if color.name() == self.color_highlight:
			color.setNamedColor(self.color_white)
		else:
			color.setNamedColor(self.color_highlight)
		self.editor.setTextBackgroundColor(color)

	def textStrikethrough(self):
		if self.isTitle(): return
		fmt = self.editor.currentCharFormat()
		fmt.setFontStrikeOut(not fmt.fontStrikeOut())
		self.editor.setCurrentCharFormat(fmt)

	def textUnderline(self):
		if self.isTitle(): return
		state = self.editor.fontUnderline()
		self.editor.setFontUnderline(not state)

	def textSizeSmall(self):
		if self.isTitle(): return
		self.editor.setFontPointSize(font_size['Small'])
	def textSizeNormal(self):
		if self.isTitle(): return
		self.editor.setFontPointSize(font_size['Normal'])
	def textSizeLarge(self):
		if self.isTitle(): return
		self.editor.setFontPointSize(font_size['Large'])
	def textSizeXLarge(self):
		if self.isTitle(): return
		self.editor.setFontPointSize(font_size['XLarge'])

	def textIndent(self):
		if self.isTitle(): return

		def indentLine(c):
			textList = c.currentList()
			if type(textList) == QTextList:
				if self.isBulletIndent(c):
					self.editor.giveBulletIndent(c, 1)
				else:
					self.editor.giveNumberIndent(c, 1)
			else: c.createList(-1)

		c = self.editor.textCursor()

		if c.hasSelection():
			temp = c.blockNumber()
			c.setPosition(c.anchor())
			diff = c.blockNumber() - temp
			direction = QTextCursor.Up if diff > 0 else QTextCursor.Down
			for n in range(abs(diff) + 1):
				indentLine(c)
				c.movePosition(direction)
		else: indentLine(c)

	def textDedent(self):
		if self.isTitle(): return

		def dedentLine(c):
			if self.isBulletIndent(c):
				self.editor.giveBulletIndent(c, -1)
			else:
				self.editor.giveNumberIndent(c, -1)

		c = self.editor.textCursor()

		if c.hasSelection():
			temp = c.blockNumber()
			c.setPosition(c.anchor())
			diff = c.blockNumber() - temp
			direction = QTextCursor.Up if diff > 0 else QTextCursor.Down
			for n in range(abs(diff) + 1):
				dedentLine(c)
				c.movePosition(direction)
		else:
			dedentLine(c)

	def isBulletIndent(self, c): # qtextedit로 옮기자
		textList = c.currentList()
		if type(textList) == QTextList:
			format = textList.format()
			indent = format.indent()
			style = format.style()
			if -3 <= style <= -1:
				return True
		return False # Number, default stentence, or Else

	def textNumOrBullet(self):
		if self.isTitle(): return

		def bulletOrNumber():
			if self.isBulletIndent(c):
				self.editor.giveNumberIndent(c)
			else:
				self.editor.giveBulletIndent(c)


		c = self.editor.textCursor()

		if c.hasSelection():
			temp = c.blockNumber()
		else:
			bulletOrNumber()

	## Mouse Event Set ##

	def eventFilter(self, source, event):
		c = self.editor.textCursor()
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
						# print('%s' %(sentence))
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