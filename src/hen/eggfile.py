#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SunGyo Kim
# Email: Kimsg1984@gmail.com
# irc.freenode #ubuntu-ko Sungyo

import re

import HTMLParser
import xml.etree.ElementTree
import IO

base = 'http://beatniksoftware.com/tomboy'


def el(name):
    if name in ['broken', 'internal', 'url']:
        namespace = '{%s/link}' % base
    elif name in ['small', 'large', 'huge']:
        namespace = '{%s/size}' % base
    else:
        namespace = '{%s}' % base
    return '{}{}'.format(namespace, name)


def parser(tag):
    text = (tag.text or '')
    # IO.pnt(text)
    # if tag.tag == el('bold'): text = '**' + text.strip() + '**'
    # elif tag.tag == el('list-item'): text = '- ' + text
    # elif tag.tag == el('url'): text = 'link: ' + text

    return text + ''.join(parser(e) for e in tag) + (tag.tail or '')


def findText(tag, keyword):
    def searching(content):
        searching_result = re.findall(r'[a-zA-Z0-9가-힣]+', IO.encode_utf(content))
        if searching_result:
            for word in searching_result:
                if word.lower() == keyword.lower(): return True

    num = len(keyword)
    if tag.text:
        if searching(tag.text): return True
    if tag.tail:
        if searching(tag.tail): return True
    for e in tag:
        if findText(e, keyword) == True:
            return True
    return False


# return text + ''.join(findKeyword(e) ) + (tag.tail or '')


class NoteFile(object):
    """wrapping ElimentTree for Tomboy XML note file"""

    def __init__(self, filename=None):
        super(NoteFile, self).__init__()
        self.__define_instance()
        # self.__register_namespace()
        if filename: self.setFile(filename)

    def __register_namespace(self):
        for name, url in [('', '%s' % base), ('link', '%s/link' % base), ('size', '%s/size' % base)]:
            xml.etree.ElementTree.register_namespace(name, url)

    def __define_instance(self):
        self.xml = ''
        self.filename = ''
        self._root = ''
        self._content = ''
        self.title = ''

    def setFile(self, filename):
        ''' 타이틀만 읽어서 시간을 줄이고 싶다면 'read_title_only = True'로! '''
        self.xml = xml.etree.ElementTree.ElementTree(file=filename)
        self.filename = filename
        self._root = self.xml.getroot()
        # self.title = IO.encode_utf(self._root.find(el('title')).text) or ''

        self._content = self._root.find(el('html'))
        print(type(self._content))

    def string(self):
        html = xml.etree.ElementTree.tostring(self._content)
        Parser = HTMLParser.HTMLParser()
        return IO.to_unicode(Parser.unescape(html))

    def plainText(self):
        content = self.string()
        content = re.sub('\n', '<bar>', content)
        content = re.sub(r'<(?!bar)(.+?)>', '', content)
        content = re.sub('<bar>', r'\n', content)
        return content

    def parse(self):
        return parser(self._content)

    def links(self):
        return set(IO.to_unicode(l.text) for l in self._content.iter(el('internal')))

    def urls(self):
        return [l.text for l in self._content.iter(el('url'))]

    def isLinkIn(self, link):
        link = IO.to_unicode(link)
        for l in self._content.iter(el('internal')):
            if l.text.lower() == link.lower(): return True
        return False

    def findText(self, text):
        return findText(self._content, text)


class Main():
    def __init__(self):
        Note = NoteFile('../../notes/test2.note')
        plain_text = Note.plainText()
        IO.pnt(plain_text)
        p_s = plain_text.splitlines()

    # for l in p_s:
    # 	if not re.findall(r'^(\s+)?$', l):
    # 		l = IO.encode_utf(l)
    # 		l_s = re.findall(r'[a-zA-Z0-9가-힣]+', l)
    # 		for w in l_s: IO.pnt(w)

    def exec_(self):
        pass


if __name__ == '__main__':
    m = Main()
    m.exec_()
