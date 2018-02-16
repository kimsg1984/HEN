#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo
import time
import shelve

def to_unicode(obj, encoding='utf-8'):
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding)
	return obj

def encode_utf(uni_str):
	return uni_str.encode('utf-8') if type(uni_str) == unicode else uni_str

def pnt(uni_str):
	print(encode_utf(uni_str))

def chec_time(func, argumenet = None):
	start = time.time()
	if argumenet:
		instance = func(argumenet)
	else:
		instance = func()
	end = time.time()
	pnt('time: {}'.format((end - start)))
	return instance

class Shelve():
	def __init__(self, filename='IO_shelve.dat'):
		db_file = filename

	def add_word(self, word, title):
		db = shelve.open(db_file)
		if db.has_key(word):
			db[word] = db[word].append(title)
		else:
			db[word] = [title]