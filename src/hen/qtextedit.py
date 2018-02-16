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

		self.__defineInstance()
		self.__setShortCut()
		# self.setLayoutDirection(2)
		self.currentChartFormat = self.currentCharFormat()
		self.textChanged.connect(self.typingHandler)

	def __defineInstance(self):
		self.is_editing_title = False
		self.LIST_STYLE_BULLET = -1
		self.LIST_STYLE_NUMBER = -2
		self.pressed_key = []

	def __setShortCut(self):
		self.setShortCut(Qt.CTRL + Qt.Key_Return, self.test)
		self.setShortCut(Qt.SHIFT + Qt.Key_Return, self.test)

	def setShortCut(self, key_assemble, method_to_connect):
		self.connect(QShortcut(QKeySequence(key_assemble), self), SIGNAL('activated()'), method_to_connect)

	def test(self):
		print('test')

	def keyPressEvent(self, QKeyEvent):
		# log.debug('QKeyEvent.key(): {}'.format(keyCode(QKeyEvent.key())))
		self.pressed_key.append(QKeyEvent.key())
		if self.keyManager(QKeyEvent): return
		QTextEdit.keyPressEvent(self, QKeyEvent)

	def keyReleaseEvent(self, QKeyEvent):
		# log.debug('QKeyEvent.key(): {}'.format(keyCode(QKeyEvent.key())))
		if QKeyEvent.key() in self.pressed_key:
			self.pressed_key.remove(QKeyEvent.key())
		QTextEdit.keyReleaseEvent(self, QKeyEvent)

	def keyManager(self, QKeyEvent):
		c = self.textCursor()
		if Qt.Key_Shift in self.pressed_key:
			if QKeyEvent.key() == Qt.Key_Return:
				c.insertText('\n')
				self.removeList(self.textCursor())
				return True

		if c.blockNumber() == 0:
			if QKeyEvent.key() == Qt.Key_Return:  # prevent Return Key Commend on Title
				self.moveCursor(QTextCursor.Down)
				self.moveCursor(QTextCursor.StartOfLine)
				if len(self.document().findBlockByLineNumber(1).text()) > 0:
					self.textCursor().insertText('\n')
					self.moveCursor(QTextCursor.Up)
				self.typingHandler(event_type='title')
				# self.setTitle()
				return True

		elif c.blockNumber() == 1 and c.columnNumber() == 0:  # prevent Backspace Key on start of  line after title
			if QKeyEvent.key() == Qt.Key_Backspace:
				if len(self.document().findBlockByLineNumber(1).text()) > 0:
					self.moveCursor(QTextCursor.Up)
					self.moveCursor(QTextCursor.EndOfLine)
					return True

		elif c.blockNumber() != 0:
			current_list = c.currentList()
			if QKeyEvent.key() == Qt.Key_Return:
				self.setCurrentCharFormat(self.currentChartFormat)

			if type(current_list) == QTextList and c.columnNumber() == 0:
				indent = current_list.format().indent()
				if QKeyEvent.key() == Qt.Key_Tab:
					self.removeList(c)
					self.giveList(self.textCursor(),1, indent = indent)
					log.debug('Tab key With List. indent: {}'.format(indent))
					return True

				if QKeyEvent.key() == Qt.Key_Backspace:
					self.removeList(c)
					self.giveList(self.textCursor(),-1, indent = indent)
					log.debug('BackSpace key With List. indent: {}'.format(indent))
					return True

		if QKeyEvent.key() in [Qt.Key_Down, Qt.Key_PageDown]:
			self.typingHandler(event_type='title')

		return False

## methods about indent ##

	def giveList(self, c, move = 0, indent = None):
		log.debug('move = {}, indent = {}'.format(move, indent))
		textList = c.currentList()

		def setList(indent):
			log.debug('move = {}, indent = {}'.format(move, indent))
			format = textList.format()
			if indent:
				indent = indent + move
			else:
				indent = format.indent() + move if format.indent() is not 0 else 0

			if indent <= 0:
				self.removeList(c)
				log.debug('remove List')
				return

			format.setIndent(indent)
			style = format.style()

			format.setStyle(-(((indent - 1) % 3) + 1))
			textList.setFormat(format)
		if type(textList) == QTextList:
			setList(indent)
		else:
			if move == -1: return
			else:
				textList = c.createList(-1)
				print(indent)
				if indent:
					setList(indent)


	def removeList(self, c):
		textList = c.currentList()
		if type(textList) == QTextList:
			format = textList.format()
			textList.remove(c.block())
			format = QTextBlockFormat()
			format.setIndent(0)
			c.setBlockFormat(format)
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
