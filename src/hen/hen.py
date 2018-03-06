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

from PyQt4.QtGui 		import *
from PyQt4.QtCore 		import *

try:
	from egg 			import Egg
	from qtextedit 		import TextEdit
	import reference
	import IO

except ImportError, err:
	log.warning("Error: %s%s" % (str(err), os.linesep))
	sys.exit(1)

event_type 	= reference.event_type
font_size 	= reference.font_size
key_type 	= reference.key_type
color 		= reference.color

def keyCode(code): return key_type[code] if key_type.has_key(code) else code

class EggEditor(QDialog):
	def __init__(self, parent=None):
		super(EggEditor, self).__init__(parent)
		self.editor = TextEdit()
		self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# self.editor.setTextInteractionFlags(Qt.LinksAccessibleByMouse) # 링크로 접속 허용??
		layout = QVBoxLayout() # appear virtically
		layout.setMargin(0)
		layout.addWidget(self.editor)
		self.menuBar = QMenuBar(self)
		layout.setMenuBar(self.menuBar)
		self.setupMenu()
		self.setLayout(layout)

		self.resize(700, 700)
		self.__defineAttributes()
		self.__setShortCut()
		self.note = Egg()

	def __defineAttributes(self):
		self.color_white = color['white']
		self.color_highlight = color['highlight']
		self.mouse_under_text = ''
		self.is_editing_title = False
		self.highlight_information = self.editor.highlight.highlight_information

	def __setShortCut(self):
		pass

	def isTitle(self):
		return True if self.editor.textCursor().blockNumber() == 0 else False

	def setupMenu(self):

		fileMenu = QMenu("&File", self)
		editMenu = QMenu("&Edit", 	self)
		styleMenu = QMenu("S&tyle", self)
		# sizeMenu = QMenu("&Size", self)
		# indentMenu = QMenu("&Indent", self)

		self.menuBar.addMenu(fileMenu)
		# self.menuBar.addMenu(editMenu)
		self.menuBar.addMenu(styleMenu)
		# self.menuBar.addMenu(sizeMenu)
		# self.menuBar.addMenu(indentMenu)
		# fileMenu.addAction("&Save...", self.saveFile, "Ctrl+S")
		# editMenu.addAction("&Copy", self.copy, "Ctrl+C")
		# editMenu.addAction("Cu&t", self.cut, "Ctrl+X")
		# editMenu.addAction("&Paste", self.paste, "Ctrl+V")

		styleMenu.addAction("&Bold", self.textBold, "Ctrl+B")
		styleMenu.addAction("&Italic", self.textItalic, "Ctrl+I")
		styleMenu.addAction("&Highlight", self.textHighlight, "Ctrl+H")
		styleMenu.addAction("&Strikethrough", self.textStrikethrough, "Ctrl+T")
		styleMenu.addAction("&Underline", self.textUnderline, "Ctrl+U")
		styleMenu.addSeparator()
		styleMenu.addAction("(&0) Normal", self.textSizeNormal, "Ctrl+0")
		styleMenu.addAction("(&1) Small", self.textSizeSmall, "Ctrl+1")
		styleMenu.addAction("(&2) Large", self.textSizeLarge, "Ctrl+2")
		styleMenu.addAction("(&3) Huge", self.textSizeHuge, "Ctrl+3")
		styleMenu.addSeparator()
		styleMenu.addAction("(&]) Indent", self.textIndent, "Alt+Right")
		styleMenu.addAction("(&[) Dedent", self.textDedent, "Alt+Left")

	def setNote(self, note):
		self.note = note
		html = note.html
		self.editor.setHtml(html)
		# self.last_block_number = self.getLastBlockNumber()


	## MenuBar Function ##
	# File Menu #

	def test(self):
		log.debug('function for testing.')

	def saveFile(self):
		html = self.editor.toHtml()
		self.note.setHtml(self.editor.toHtml())
		self.note.saveFile()

	# Edit Menu #


	# Style Menu #
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
	def textSizeHuge(self):
		if self.isTitle(): return
		self.editor.setFontPointSize(font_size['Huge'])

	def textIndent(self):
		if self.isTitle(): return

		def indentLine(c):
			textList = c.currentList()
			if type(textList) == QTextList:
				self.editor.giveList(c, 1)
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
			self.editor.giveList(c, -1)

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

	## Event Set ##

	def eventFilter(self, source, event):
		if 		event.type() == QEvent.MouseMove: self._mouseEventFilter(event)
		elif 	event.type() == QEvent.KeyRelease: self._keyReleaseEventFilter(event)
		elif 	event.type() == QEvent.KeyPress: self._keyPressEventFilter(event)

		return self.editor.eventFilter(source, event)

	def _mouseEventFilter(self, event):
		""""""
		def eventNoButton():
			virtual_cursor = self.editor.cursorForPosition(mouse_pos)  # 설렉션 잡을 때 마다 생성해줘야 함.

			virtual_cursor_move = self.editor.cursorForPosition(mouse_pos)
			virtual_cursor_move.movePosition(virtual_cursor.StartOfWord)
			cursor_rect_start = self.editor.cursorRect(virtual_cursor_move)
			virtual_cursor_move.movePosition(virtual_cursor.EndOfWord)
			cursor_rect_end = self.editor.cursorRect(virtual_cursor_move)

			word_position = (cursor_rect_start.x(), cursor_rect_end.x(),
							 cursor_rect_start.top(), cursor_rect_start.top() + cursor_rect_start.height())
			allow_point = 8

			virtual_cursor.select(QTextCursor.WordUnderCursor)

			self.virtual_cursor = virtual_cursor
			text = virtual_cursor.selectedText()
			in_wide = word_position[0] - allow_point <= mouse_pos.x() <= word_position[1] + allow_point
			in_height = word_position[2] - allow_point <= mouse_pos.y() <= word_position[3] + allow_point

			if in_wide and in_height:
				if len(text) > 0:
					if self.mouse_under_text == text:
						if self.editor.viewport().cursor().shape() == 4 \
								and virtual_cursor.charFormat().isAnchor():
							self.editor.viewport().setCursor(QCursor(Qt.PointingHandCursor))
					else:
						sentence = 'selectedText: %s' % text
						sentence = sentence.encode('utf-8')
						self.mouse_under_text = text

						if virtual_cursor.charFormat().isAnchor():
							log.info(virtual_cursor.charFormat().anchorHref())
							self.editor.viewport().setCursor(QCursor(Qt.PointingHandCursor))
						else:
							self.editor.viewport().setCursor(QCursor(Qt.IBeamCursor))
				else:
					self.mouse_under_text = ''
					pass  # do other stuff
			else:
				self.editor.viewport().setCursor(QCursor(Qt.IBeamCursor))
		def eventNoButton2():
			def isPositionInLink():
				if block_number in self.highlight_information:
					highlight_info = self.highlight_information[block_number]
					highlight_info.sort()
					for info_list in highlight_info:
						print(cursor_number_in_block, info_list)
						if info_list[0] <= cursor_number_in_block:
							if cursor_number_in_block <= info_list[1]:

								return True
						else: break
				return False

			virtual_cursor 		= self.editor.cursorForPosition(mouse_pos)  # 설렉션 잡을 때 마다 생성해줘야 함.
			block_number 		= virtual_cursor.block().blockNumber()
			cursor_number_in_block	= virtual_cursor.positionInBlock()
			virtual_cursor_move = self.editor.cursorForPosition(mouse_pos)
			virtual_cursor_move.movePosition(virtual_cursor.StartOfWord)
			cursor_rect_start 	= self.editor.cursorRect(virtual_cursor_move)
			virtual_cursor_move.movePosition(virtual_cursor.EndOfWord)
			cursor_rect_end 	= self.editor.cursorRect(virtual_cursor_move)

			word_position 		= (cursor_rect_start.x(), cursor_rect_end.x(),
									cursor_rect_start.top(), cursor_rect_start.top() + cursor_rect_start.height())
			allow_point 		= 8

			virtual_cursor.select(QTextCursor.WordUnderCursor)

			self.virtual_cursor = virtual_cursor
			text 				= virtual_cursor.selectedText()
			in_wide 			= word_position[0] - allow_point <= mouse_pos.x() <= word_position[1] + allow_point
			in_height 			= word_position[2] - allow_point <= mouse_pos.y() <= word_position[3] + allow_point

			if in_wide and in_height:
				if len(text) > 0:
					isPositionInLink()
					if self.mouse_under_text == text:
						# and virtual_cursor.charFormat().isAnchor():
						if self.editor.viewport().cursor().shape() == Qt.IBeamCursor \
								and isPositionInLink():
							self.editor.viewport().setCursor(QCursor(Qt.PointingHandCursor))
					else:
						sentence = 'selectedText: %s' % text
						sentence = sentence.encode('utf-8')
						self.mouse_under_text = text

						if virtual_cursor.charFormat().isAnchor():
							log.info(virtual_cursor.charFormat().anchorHref())
							self.editor.viewport().setCursor(QCursor(Qt.PointingHandCursor))
						else:
							self.editor.viewport().setCursor(QCursor(Qt.IBeamCursor))
				else:
					self.mouse_under_text = ''
					pass  # do other stuff
			else:
				self.editor.viewport().setCursor(QCursor(Qt.IBeamCursor))

		mouse_pos = event.pos()
		if event.buttons() == Qt.NoButton:
			# eventNoButton()
			eventNoButton2()

	def _keyReleaseEventFilter(self, event):
		# print(key_type[event.key()])
		pass

	def _keyPressEventFilter(self, event):
		"""
	    """
		# print(key_type[event.key()])
		# print(self.editor.textCursor().blockNumber(),self.last_block_number)

		# def adjust
