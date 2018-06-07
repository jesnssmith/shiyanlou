# -*- coding:utf-8 -*-

import re
import datetime

pattern = ( r''
			r'(\d+.\d+.\d+.\d+)\s-\s-\s'
			r'\[(.+)\]\s'
			r'"GET\s(.+)\s\w+/.+"\s'
			r'(\d+)\s'
			r'(\d+)\s'
			r'"(.+)"\s'
			r'"(.+)"')

def open_parser(filename):
	with open(filename) as logfile:
		pattern = ( r''
					r'(\d+.\d+.\d+.\d+)\s-\s-\s'
					r'\[(.+)\]\s'
					r'"GET\s(.+)\s\w+/.+"\s'
					r'(\d+)\s'
					r'(\d+)\s'
					r'"(.+)"\s'
					r'"(.+)"')
		parsers = re.findall(pattern, logfile.read())
	return parsers

def main():

	logs = open_parser('/home/shiyanlou/Code/nginx.log')
	date = datetime.date(2017, 1, 11)
	ip_dict = {}
	url_dict = {}
	for log in logs:
		if datetime.datetime.strptime(log[1][:11], "%d/%b/%Y").date() == datetime.date(2017,1,11):
			if ip_dict.get(log[0]):
				ip_dict[log[0]] += 1
			else:
				ip_dict[log[0]] = 1

		if log[3] == '404':
			log2 = log[2].split(' ')[0]
			if url_dict.get(log2):
				url_dict[log2] += 1
			else:
				url_dict[log2] =1

 
	ip_dict = sorted(ip_dict.items(), key = lambda x:x[1], reverse = True)

	url_dict =sorted(url_dict.items(), key = lambda x: x[1], reverse =True)
	# return url_dict
	return {ip_dict[0][0] : ip_dict[0][1]}, {url_dict[0][0] : url_dict[0][1]}

if __name__ == '__main__':
	id_dict, url_dict = main()
	print(id_dict,url_dict)
	# url_dict = main()
	# print(url_dict)