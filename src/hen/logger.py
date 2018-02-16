# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# # Author: SunGyo Kim
# # Email: Kimsg1984@gmail.com
# # irc.freenode #ubuntu-ko Sungyo

import logging

# class Log(logging.Logger):
# 	def __init__(self, name = 'HaniBaram'):
# 		super(Log, self).__init__(name)
# 		fomatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s|%(levelname)s]\t %(message)s')
# 		streamHandler = logging.StreamHandler()
# 		streamHandler.setFormatter(fomatter)
# 		self.addHandler(streamHandler)
# 		# self.setLevel(logging.DEBUG)
# 		self.setLevel(logging.INFO)

# class Main():
# 	def __init__(self):
# 		self.l = Log()

# 	def exec_(self):
# 		self.l.debug('test')

# if __name__ == '__main__':
# 	m = Main()
# 	m.exec_()


import logging.config

def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class Logger():
    def __init__(self):
        # logging.config.fileConfig('logging.conf')
        self.logr = logging.getLogger('root')
        self.logr.setLevel(logging.INFO)
