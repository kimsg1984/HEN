#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

import re

def debug(text):
	#print(text)
	pass

class MarkupToList(object):
	"""docstring for MarkupToList"""
	def __init__(self, markup_string):
		super(MarkupToList, self).__init__()
		self.markup_string = markup_string
		self.short_tag = False

	@classmethod
	def _markup_string_to_list_recursion(cls, markup_split_reversed, result = []):

		def parse_attribute(attribute):
			attribute_string = ' '.join(attribute)
			return _attribute_recurion(attribute_string)

		def _attribute_recurion(attribute_string, result = {}):

			equel_offset = attribute_string.find('=')

			if equel_offset != -1:
				attribute_name =  attribute_string[0:equel_offset].strip()
				attribute_string =  attribute_string[equel_offset + 1:].strip()
				if attribute_string[0] == '"': # open quote
					quote_offset = attribute_string.find('"', 1)
					if quote_offset != -1:
						value =  attribute_string[1:quote_offset].strip() # striped quote
						attribute_string =  attribute_string[quote_offset+1:].strip()
					else:
						value = attribute_string[1:].strip() # striped  pre-quote
						attribute_string = ''
				else:
					space_offset = attribute_string.find(' ')
					if space_offset != -1:
						value =  attribute_string[0:space_offset].strip()
						attribute_string =  attribute_string[space_offset:].strip()
					else:
						value = attribute_string
						attribute_string = ''
			else:
				attribute_name =  attribute_string
				value = ''
				attribute_string = ''

			value_splited = value.split(';')

			if len(value_splited) > 1:
				if not value_splited[-1]:
					value_splited.pop()
					result[attribute_name] = [(':'.join([v_split.strip() for v_split in v.split(':')])).strip() for v in value_splited]
			else:
				result[attribute_name] = [value]

			if attribute_string:
				return _attribute_recurion(attribute_string, result = result)
			else:
				return result

		def result_append(entity):
			result.append(entity)

		def return_loop(markup_split_reversed, result):
			if markup_split_reversed:
				if len(markup_split_reversed) != 0:
					return markup_split_reversed, result
			return None, result

		debug('[LOOP START]')
		entity_result = ['', '', []]
		entity_split = markup_split_reversed.pop().split('>')

		tag = entity_split[0].split(' ')
		if entity_split[0][0] == '!':
			debug('[주석] {}'.format(tag[0]))
			pass
		elif entity_split[0][0] != '/':
			debug('[태그열기] {}'.format(tag[0]))
			if tag[-1] == '/':
				debug('	[짧은 태그]')
				if tag[0] == 'br': # <br />
					entity_result = [tag[0], '', '']
				else:
					entity_result = [tag[0], parse_attribute(tag[1:-1]), '']
				result_append(entity_result)
				return return_loop(markup_split_reversed, result)

			# 열린 태그 #
			elif len(tag) == 1: # no attribute
				entity_result[0], entity_result[1]  = tag[0], ''

			else: # with attribute
				entity_result[0], entity_result[1] = tag[0], parse_attribute(tag[1:])

			if len(entity_split[1]) != 0: # add content
				entity_result[2].append(entity_split[1])

			if markup_split_reversed[-1][0] == '/': # tag closed
				close_tag = markup_split_reversed.pop()
				debug('[태그닫기] {}'.format(close_tag))
				result_append(entity_result)

			else: # sub_result #
				while markup_split_reversed[-1][0] != '/':
					debug('	[서브태그 열기]: {}'.format(tag[0]))
					markup_split_reversed, sub_result = cls._markup_string_to_list_recursion(markup_split_reversed, result = [])
					entity_result[2]+= sub_result
					debug('	[/서브태그 닫기]: {}'.format(tag[0]))

				close_tag = markup_split_reversed.pop()
				debug('[태그닫기] {}'.format(close_tag))
				result_append(entity_result)

		return return_loop(markup_split_reversed, result)

	def markupToList(self, markup_string):
		declaration = None
		markup_string = re.sub('\n', '', markup_string)
		markup_string_split = markup_string.split('<')
		if len(markup_string_split[0]) == 0 : del(markup_string_split[0])
		markup_string_split.reverse() # to use pop

		first_entity = markup_string_split.pop()
		first_entity_split = first_entity.split()

		if first_entity_split[0][0] == '!':
			declaration = re.sub(r'\>$', '', first_entity)
		else:
			markup_string_split.append(first_entity)

		result = list((self._markup_string_to_list_recursion(markup_string_split, result = [declaration])))
		if result[0] == None: result = result[1]
		return result

class ListToMarkup(object):
	"""docstring for ListToMarkup
	"""
	def __init__(self, markup_list, short_tag = False):
		super(ListToMarkup, self).__init__()
		self.markup_list = markup_list
		self.short_tag = short_tag
		self.with_declaration = True
		self.paragraph_tag = ['p']
		self.delete_list = []
		self.strip_list_sensitive = []
		self.strip_list_forced = []

	def manageAttribute(self, tag, attribute_dict):
		"""
		For overriding
		defult: return attribute_dict
		"""
		return attribute_dict

	def _assembleAttribute(self, tag, attribute_dict):
		result = ''
		attribute_dict_managed = self.manageAttribute(tag, attribute_dict)
		for attribute_name in attribute_dict_managed:
			value = attribute_dict_managed[attribute_name]
			if type(value) == str:
				value_string = value
			else: # should be list
				if len(value) == 1:
					value_string = value[0]
				elif len(value) > 1:
					value_string = '; '.join(v for v in value) + ';'

			result += '{}="{}" '.format(attribute_name, value_string)

		return result.strip()

	def _assembleOrder(self, tag, attribute, content):
		return self.assembleOrder(tag, attribute, content)

	def assembleOrder(self, tag, attribute, content):
		"""
		For overriding
			# default: return '\n<{}>{}</{}>'.format((tag + ' ' + attribute).strip(), content, tag)
		"""

		return '\n<{}>{}</{}>'.format((tag + ' ' + attribute).strip(), content, tag)

	def _assembelOrderShortTag(self, tag, attribute):
		return self.assembelOrderShortTag(tag, attribute)

	def assembelOrderShortTag(self, tag, attribute):
		"""
		For overriding, only self.short_tag == True
			# default: return '\n<{} />'.format((tag + ' ' + attribute).strip())
		"""
		return '\n<{} />'.format((tag + ' ' + attribute).strip())

	def listToMarkup(self):
		result = ''
		ml = self.markup_list

		if self.with_declaration:
			if type(ml[0]) == str:
				result += '<{}>'.format(ml[0])

		result = self._listToMarkup_recusion(ml[1], result)
		return result.strip()

	def _listToMarkup_recusion(self, entity, result=''):
		def getContent(content):
			if type(content[0]) == str:
				content = content[0]
			else:
				content = ''.join(self._listToMarkup_recusion(c) for c in content)

			return content

		tag = entity[0]
		attribute = entity[1]
		content = entity[2]

		if tag in self.delete_list: return result

		if type(attribute) == dict:
			if attribute:
				attribute = self._assembleAttribute(tag, attribute)
			else:
				attribute = ''

		if content:
			if tag in self.strip_list_forced:
				result += getContent(content); return result
			if tag in self.paragraph_tag and not attribute:
				result += getContent(content) + '\n'; return result
			if tag in self.strip_list_sensitive and not attribute:
				result += getContent(content); return result

			content = getContent(content)

		else: # short tag
			if self.short_tag:
				result += self._assembelOrderShortTag(tag, attribute)
				return result

		result += self._assembleOrder(tag, attribute, content)


		return result

	def showTree(self):

		pass

class HtmlAssembler(ListToMarkup, MarkupToList):
	"""docstring for HtmlToNoteFileFormat

	overriding able function:
		manageAttribute()
		assembleOrder()
		assembleOrderShortTag()

	values :
		self.delete_list = []
			add string what you want to delete.
		self.strip_list = []
		add string what you want to strip.

	"""

	def __init__(self, html_string):
		self.markup_list = self.markupToList(html_string)

	def manageAttribute(self, tag, attribute_dict):
		return attribute_dict