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
import signal
sys.setdefaultencoding('utf-8')
# sys.setrecursionlimit(10000)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
	 from highlighter import Highlighter
except ImportError, err:
 	sys.stderr.write("Error: %s%s" % (str(err), os.linesep))
 	sys.exit(1)

try:
	from note import Note
	from reference import event_type, font_size

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

		# self.highlight = Highlighter(self.editor.document())
		# self.highlight.addKeyword('class')
		# self.highlight.addKeyword('clas.cs')

		self.resize(500, 500)

		self.mouse_under_text = ''
		self.is_editing_title = False
		self.note = Note()
		self.currentChartFormat = self.editor.currentCharFormat()
		self.editor.textChanged.connect(self.typingHandler)

	def setupMenu(self):

		fileMenu = QMenu("&File", self)
		self.menuBar.addMenu(fileMenu)
		fileMenu.addAction("&Save...", 		self.saveFile, 		"Ctrl+S")

		editMenu = QMenu("&Edit", 	self)
		self.menuBar.addMenu(editMenu)
		editMenu.addAction("&Bord", 		self.textBold, 		"Ctrl+B")
		editMenu.addAction("&Italic", 		self.textItalic, 		"Ctrl+I")
		editMenu.addAction("&Highlight", self.textHighlight, 	"Ctrl+H")
		editMenu.addAction("&Strikethrough", self.textStrikethrough, "Ctrl+T")
		editMenu.addAction("&Underline", self.textUnderline, 	"Ctrl+U")
		editMenu.addSeparator()
		editMenu.addAction("S&mall", 		self.textSizeSmall, 	"Ctrl+1")
		editMenu.addAction("&Normal", 	self.textSizeNormal, "Ctrl+2")
		editMenu.addAction("&Large", 		self.textSizeLarge, 	"Ctrl+3")
		editMenu.addAction("&X-Large", 	self.textSizeXLarge, "Ctrl+4")
		editMenu.addSeparator()
		editMenu.addAction("Indent", 		self.textIndent, 		"Alt+Right")
		editMenu.addAction("Dedent", 		self.textDedent, 	"Alt+Left")

	def setNote(self, note):
		self.note = note
		html = note.html
		self.editor.setHtml(html)
		c = self.editor.textCursor()
		# 타이틀이나 여는 시간등도 설정할 것.

	## MenuBar Function ##
	def saveFile(self):
		html = self.editor.toHtml()
		self.note.setHtml(self.editor.toHtml())
		self.note.saveFile()

	def textBold(self):
		if self.editor.fontWeight() == QFont.Bold:
			self.editor.setFontWeight(QFont.Normal)
		else:
			self.editor.setFontWeight(QFont.Bold)

	def textItalic(self):
		state = self.editor.fontItalic()
		self.editor.setFontItalic(not state)

	def textHighlight(self):
		color = self.editor.textBackgroundColor()
		if color.name() == '#ffff00':
			color.setNamedColor('#ffffff')
		else:
			color.setNamedColor('#ffff00')
		self.editor.setTextBackgroundColor(color)

	def textStrikethrough(self):
		fmt = self.editor.currentCharFormat()
		fmt.setFontStrikeOut(not fmt.fontStrikeOut())
		self.editor.setCurrentCharFormat(fmt)

	def textUnderline(self):
		state = self.editor.fontUnderline()
		self.editor.setFontUnderline(not state)

	def textSizeSmall(self): 		self.editor.setFontPointSize(font_size['Small'])	
	def textSizeNormal(self): 	self.editor.setFontPointSize(font_size['Normal'])
	def textSizeLarge(self): 		self.editor.setFontPointSize(font_size['Large'])
	def textSizeXLarge(self): 	self.editor.setFontPointSize(font_size['XLarge'])

	def textIndent(self):
		def indentLine(c):
			textList = c.currentList()

			if type(textList) == QTextList:
				format = textList.format()
				indent = format.indent()
				style = format.style()
				print('style: {}, indent: {}'.format(style, indent))

				format.setIndent(indent + 1)
				format.setStyle(-(((indent) % 3) +1))
				textList.setFormat(format)
				# print('indent:{}, style:{}'.format(format.indent(), format.style()))
				# c.createList(format)
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
		def dedentLine(c):
			textList = c.currentList()
			if type(textList) == QTextList:
				format = textList.format()
				indent = format.indent()
				style = format.style()

				format.setIndent(indent -1)
				print('style: {}, indent: {}'.format(style, indent))
				format.setStyle(-(((indent-2) % 3) +1))
				textList.setFormat(format)
				if indent <= 1: 
					format.setIndent(0)
					textList.setFormat(format)
					textList.remove(c.block())

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

 	# typingHandler #

	def typingHandler(self, event_type = None):
		def wiki_rule():
			pass

		def setTitle():
			c.movePosition(c.Start)
			c.select(QTextCursor.LineUnderCursor)
			selected_text = c.selectedText()
			format = c.charFormat()
			format.setFontPointSize(20)
			format.setForeground(Qt.blue)
			format.setFontUnderline(True)
			c.setCharFormat(format)
			if selected_text != selected_text.trimmed():
				c.insertText(selected_text.trimmed())

 		c = self.editor.textCursor()
		if c.hasSelection(): return True
		
		if c.blockNumber() == 0:
			if self.is_editing_title == False:
				self.is_editing_title = True
				setTitle()
			return True

		if c.blockNumber() != 0 and self.is_editing_title == True: # 제목편집 완료
			self.is_editing_title = False
			setTitle()
		if event_type == 'title': return True

 		c_selected = self.editor.textCursor()
		if self.editor.textCursor().atBlockStart():
			self.editor.setCurrentCharFormat(self.currentChartFormat)
		elif self.editor.textCursor().atBlockEnd():
			self.editor.setCurrentCharFormat(self.currentChartFormat)
		
		else:
			current_format = c.charFormat()
			c.movePosition(c.Right)
			right_format = c.charFormat()
			 
			#weight (bold)
			if current_format.fontWeight() != right_format.fontWeight():
				current_format.setFontWeight(QFont.Normal)

			# italac
			if current_format.fontItalic() != right_format.fontItalic():
				current_format.setFontItalic(False)

			# strikethrough
			if current_format.fontStrikeOut() != right_format.fontStrikeOut():
				current_format.setFontStrikeOut(False)

			# highlight
			if current_format.background().color().name() != right_format.background().color().name():	
				color = QColor()
				color.setNamedColor('#ffffff')
				current_format.setBackground(QBrush(color))
	
			self.editor.setCurrentCharFormat(current_format)

	## Event Set ##

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
		
		# if event.type() not in [77, 1, 12]: print(event_type[event.type()])

		if event.type() == QEvent.KeyRelease:
			if event.key() in [Qt.Key_Down, Qt.Key_PageDown]:
				self.typingHandler(event_type = 'title')

		if event.type() == QEvent.KeyPress:
			if event.key() == Qt.Key_Return:
				self.editor.setCurrentCharFormat(self.currentChartFormat)

		return self.editor.eventFilter(self, event)
