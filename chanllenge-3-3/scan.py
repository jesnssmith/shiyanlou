#!/usr/env/bin python3
# -*- coding: utf-8 -*-

import sys
import getopt

def get_argv(argv):
	try:
		opts, args =getopt.getopt(argv, '', ['host=', 'port='])
	except getopt.GetoptError:
		print('Parameter Error')

	for opt, arg in opts:
		if opt == '--host':
			host = arg
		elif opt == '--port':
			port = arg
		else:
			continue
	return host, port


if __name__ == '__main__':
	host, port = get_argv(sys.argv[1:])
	port = port.split('-')
	# if len(port) == 2:
	# 	port = range(int(port[0], int(port[1])+1))
	# else:
	# 	port = int(port)
	port = (int(x) for x in port)
	print(host, ':', port)