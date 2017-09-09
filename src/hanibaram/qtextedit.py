#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

import logging

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from reference import key_type

log = logging.getLogger(__name__)
def keyCode(code): return key_type[code] if key_type.has_key(code) else code

class TextEdit(QTextEdit):
	def __init__(self, parent=None):
		super(TextEdit, self).__init__(parent)

		self.is_editing_title = False
		self.currentChartFormat = self.currentCharFormat()
		self.textChanged.connect(self.typingHandler)

	def keyPressEvent(self, QKeyEvent):
		log.debug('QKeyEvent.key(): {}'.format(keyCode(QKeyEvent.key())))
		c = self.textCursor()

		if c.blockNumber() == 0:
			if QKeyEvent.key() == Qt.Key_Return:  # prevent Return Key on Title
				self.moveCursor(QTextCursor.Down)
				self.typingHandler(event_type='title')
				# self.setTitle()
				return

		elif c.blockNumber() == 1 and c.blockNumber() == 1: # prevent Backspace Key on start of  line after title
			if QKeyEvent.key() == Qt.Key_Backspace:
				self.moveCursor(QTextCursor.Up)
				self.moveCursor(QTextCursor.EndOfLine)
				return

		elif c.blockNumber() != 0:
			if QKeyEvent.key() == Qt.Key_Return:
				self.setCurrentCharFormat(self.currentChartFormat)
				current_list = c.currentList()
				if current_list:
					bullet = self.isBulletIndent(c)
					# current_list.remove(c.block())

		if QKeyEvent.key() in [Qt.Key_Down, Qt.Key_PageDown]:
			self.typingHandler(event_type='title')

		QTextEdit.keyPressEvent(self, QKeyEvent)

	## methods about indent ##
	def isBulletIndent(self, c):
		textList = c.currentList()
		if type(textList) == QTextList:
			format = textList.format()
			indent = format.indent()
			style = format.style()
			if -3 <= style <= -1:
				return True
		return False # Number or default stentence

	def giveBulletIndent(self, c,move = 0, indent = None):
		textList = c.currentList()
		if type(textList) == QTextList:
			format = textList.format()
			indent = format.indent() + move if format.indent() is not 0 else 0

			if indent <= 0:
				format.setIndent(0)
				textList.setFormat(format)
				textList.remove(c.block())
				return

			format.setIndent(indent)
			style = format.style()
			format.setStyle(-(((indent-1) % 3)+1))
			textList.setFormat(format)
			log.debug('giveBulletIndent: style: {}, indent: {}'.format(style, indent))
		else:
			c.createList(-1)

	def giveNumberIndent(self, c, move = 0, indent = None):
		textList = c.currentList()
		if type(textList) == QTextList:
			format = textList.format()
			indent = format.indent() + move if format.indent() is not 0 else 0

			if indent <= 0:
				format.setIndent(0)
				textList.setFormat(format)
				textList.remove(c.block())
				return

			format.setIndent(indent)
			style = format.style()
			format.setStyle(-(((indent-1) % 5) + 4))
			textList.setFormat(format)
			log.debug('giveNumberIndent: style: {}, indent: {}'.format(style, indent))
		else:
			if move is not -1 : c.createList(-4)

	def giveIndent(self, c,move = 0,bullet_indent = True, indent = None):
		
		textList = c.currentList()
		if type(textList) == QTextList:
			format = textList.format()
			indent = format.indent() + move if format.indent() is not 0 else 0

			if indent <= 0:
				format.setIndent(0)
				textList.setFormat(format)
				textList.remove(c.block())
				return

			format.setIndent(indent)
			style = format.style()
			format.setStyle(-(((indent-1) % 3)+1))
			textList.setFormat(format)
			log.debug('giveBulletIndent: style: {}, indent: {}'.format(style, indent))
		else:
			c.createList(-1)

	def typingHandler(self, event_type = None):
		def setTitle():
			# c = self.textCursor()
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
		# log.debug('')
		def wiki_rule():
			pass

		c = self.textCursor()
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

		c_selected = self.textCursor()
		if self.textCursor().atBlockStart():
			self.setCurrentCharFormat(self.currentChartFormat)
		elif self.textCursor().atBlockEnd():
			self.setCurrentCharFormat(self.currentChartFormat)

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
				color.setNamedColor(self.color_white)
				current_format.setBackground(QBrush(color))

			self.setCurrentCharFormat(current_format)
