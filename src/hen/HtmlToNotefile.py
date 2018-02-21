#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo
 
import re

import MarkupAssembler
import reference
from pprint import pprint

# filename = 'test_basic.html'
filename = 'test_full.html'

# should pull from 'scr/hen/reference.py' when imply

font_size = reference.font_size

# {'li': {'style': set(['-qt-block-indent:0',
#                       'margin-bottom:0px',
#                       'margin-left:0px',
#                       'margin-right:0px',
#                       'margin-top:0px',
#                       'text-indent:0px'])},
#  'ol': {'style': set(['-qt-list-indent: 2',
#                       '-qt-list-indent: 3',
#                       '-qt-list-indent: 4',
#                       'margin-bottom: 0px',
#                       'margin-left: 0px',
#                       'margin-right: 0px',
#                       'margin-top: 0px']),
#         'type': set(['A', 'a', 'i'])},
#  'p': {'style': set(['-qt-block-indent:0',
#                      '-qt-paragraph-type:empty',
#                      'margin-bottom:0px',
#                      'margin-left:0px',
#                      'margin-right:0px',
#                      'margin-top:0px',
#                      'text-indent:0px'])},
#  'span': {'style': set(['background-color:#ffff00',
#                         'color:#0000ff',
#                         'font-size:15pt',
#                         'font-size:20pt',
#                         'font-size:9pt',
#                         'font-style:italic',
#                         'font-weight:600',
#                         'text-decoration: line-through',
#                         'text-decoration: underline'])},
#  'ul': {'style': set(['-qt-list-indent: 1',
#                       '-qt-list-indent: 2',
#                       '-qt-list-indent: 3',
#                       '-qt-list-indent: 4',
#                       '-qt-list-indent: 5',
#                       '-qt-list-indent: 6',
#                       '-qt-list-indent: 7',
#                       '-qt-list-indent: 8',
#                       'margin-bottom: 0px',
#                       'margin-left: 0px',
#                       'margin-right: 0px',
#                       'margin-top: 0px']),
#         'type': set(['circle', 'square'])}}

class HtmlToNoteFileFormat(MarkupAssembler.HtmlAssembler):
	def __init__(self, html_string):
		self.markup_list = self.markupToList(html_string)
		self.short_tag = True
		self.with_declaration = False
		self.paragraph_tag = ['p'] # skip entity including attribute
		self.delete_list = ['head']
		self.strip_list_sensitive = ['p']
		self.strip_list_forced = ['html', 'body']
		self.attribute_gathering_dict = {}
		self.manage_attribute_first_function = True

		margin_default = [
			'margin-bottom:0px', 'margin-left:0px', 'margin-right:0px', 'margin-top:0px',
		]

		self.attribute_set_default = {
			'p' : {'style' : margin_default + ['-qt-block-indent:0', 'text-indent:0px']},
			'ul': {'style' : margin_default},
			'li': {'style' : margin_default + ['-qt-block-indent:0','text-indent:0px']},
			'ol': {'style' : margin_default},
			}

		self.attribute_set_delete = { # should overload dict and list.
			'p' : {'style' : ['-qt-user-state:0', '-qt-paragraph-type:empty']},
			'ul' : ['type'],
			'ol' : ['type'],
			}

		self.attribute_set_correspondence = {
			# 'p' 	: 	{'style' : { '-qt-paragraph-type:empty': '' }}, ֒
			'span' 	:	{'style' : {
								'font-size:{}pt'.format(font_size['Small']) : 'size:small',
								'font-size:{}pt'.format(font_size['Normal']): 'size:normal',
								'font-size:{}pt'.format(font_size['Large']) : 'size:large',
								'font-size:{}pt'.format(font_size['Huge']) 	: 'size:huge',
								'background-color:#ffff00' : 'highlight', 'font-weight:600' : 'bold',
								'text-decoration:line-through' : 'strikethrough',
								'text-decoration:underline' : 'underline', 'font-style:italic' : 'italic'}
						},
			'ul'	: 	{'style' : {'-qt-list-indent' : 'indent'}},
			'ol'	: 	{'style' : {'-qt-list-indent' : 'indent'}},
		}

	def manageAttribute(self, tag, attribute_dict):
		return self._attributeFactory(tag, attribute_dict)

	def _attributeFactory(self, tag, attribute_dict):

		for attribute_name in attribute_dict.keys():
			attribute_values = list(attribute_dict[attribute_name])

			if tag in self.attribute_set_default:
				if attribute_name in self.attribute_set_default[tag]:
					attribute_values = list(set(attribute_values)
														  - set(self.attribute_set_default[tag][attribute_name]))

			if tag in self.attribute_set_delete:
				if attribute_name in self.attribute_set_delete[tag]:
					if type(self.attribute_set_delete[tag]) == dict:
						attribute_values = list(set(attribute_values)
															  - set(self.attribute_set_delete[tag][attribute_name]))
					elif type(self.attribute_set_delete[tag]) == list:
						attribute_values = []

			if tag in self.attribute_set_correspondence:
				if attribute_name in self.attribute_set_correspondence[tag]:
					correspondence_dict = self.attribute_set_correspondence[tag][attribute_name]
					for correspondence in correspondence_dict:
						correspondence_value = correspondence_dict[correspondence]
						attribute_values_str = ';'.join(attribute_dict[attribute_name])


						if ':' in correspondence:
							if correspondence in attribute_values:
								attribute_values.remove(correspondence)
								attribute_values.append(correspondence_value)
						else:
							attribute_values_str = ';'.join(attribute_values)
							if len(re.findall(correspondence, attribute_values_str)) > 0:
								attribute_values_str = re.sub(correspondence, correspondence_value, attribute_values_str)
								attribute_values = attribute_values_str.split(';')

			attribute_dict[attribute_name] = attribute_values

		attribute_name_list = [attribute_name for attribute_name in attribute_dict]
		for attribute_name in attribute_name_list:
			if len(attribute_dict[attribute_name]) == 0: del(attribute_dict[attribute_name])

		return attribute_dict

	def assembelOrderShortTag(self, tag, attribute):
		if tag is not 'br':
			# return '\n'
			return ''
		else:
			return '\n<{} />'.format((tag + ' ' + attribute).strip())

	def assembleOrder(self, tag, attribute, content):
		"""
		For overriding
			# default: return '\n<{}>{}</{}>'.format((tag + ' ' + attribute).strip(), content, tag)
		"""
		result = ''

		result += '<{}>'.format((tag + ' ' + attribute).strip())
		if tag in ['ul', 'ol']: result += '\n'
		result += '{}'.format(content)
		result += '</{}>'.format(tag)

		if tag in ['ul', 'li', 'ol']: result += '\n'
		return result

class Main():
	def __init__(self):
		file_content = open(filename).read()
		self.m = HtmlToNoteFileFormat(file_content)
		result = self.m.listToMarkup()
		# print(result)


	def exec_(self):
		pass 

if __name__ == '__main__':
	m = Main()
	m.exec_()