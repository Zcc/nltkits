#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import jieba
from operator import itemgetter


def getrawtext(xlsxfile='static/tmp/tmp.xlsx', columnnum=2):
    data = xlrd.open_workbook(xlsxfile)
    rawtext = open('static/tmp/rawtext.txt', 'w')
    table = data.sheets()[0]
    rownum = table.nrows
    lines = []
    for i in xrange(1, rownum):
        line = str(table.row(i)[columnnum].value).strip()
        if line != '':
            rawtext.write(line + '\n')
            lines.append(line)
    return lines


def frequency(lines=open('static/tmp/rawtext.txt').readlines()):
    wdic = {}
    for line in lines:
        words = jieba.cut(line.strip())
        for word in words:
            if wdic.has_key(word):
                wdic[word] += 1
            else:
                wdic[word] = 1
    sortline = sorted(wdic.iteritems(), key=itemgetter(1), reverse=True)
    fi = open('static/tmp/frequency.txt', 'w')
    for line in sortline:
        fi.write(str(line[0]) + '\t' + str(line[1]) + '\n')
    fi.close()
    return sortline


def get_xlsx_frequency(xlsxfile='static/tmp/tmp.xlsx', columnnum=2):
    return frequency(getrawtext(xlsxfile, columnnum))
