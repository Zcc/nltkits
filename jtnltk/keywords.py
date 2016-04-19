#!/usr/bin/python
# -*- coding: utf-8 -*-
from snownlp import SnowNLP
from snownlp import summary

def keywords(text,num):
	s = SnowNLP(text.decode('utf8'))
	#st = frequency.Stopwords()
	return s.keywords(num)

if __name__ == '__main__':
	text = open('../static/tmp/rawtext.txt').read()
	num = 50
	keys = keywords(text,num)
	stops = [s.strip() for s in open('../dic/stopwords.dic').readlines()]
	for k in keys:
		print k
		if k in stops:
			print k

