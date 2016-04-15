#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.dom.minidom
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def xmlprocess(data):
    tmpfile = '../tmp/tmp.xml'
    f = open(tmpfile, 'w')
    f.write(data)
    f.close()
    dom = xml.dom.minidom.parse(tmpfile)
    root = dom.documentElement
    segs = root.getElementsByTagName("Question")
    print len(segs)
    content = []
    for seg in segs:
        content.append(seg.getElementsByTagName(
            'FinalSeg')[0].childNodes[0].data)
    return content


def Stopwords():
    return [s.strip() for s in open('dic/stopwords.dic').readlines()]


def statistics(data):
    content = xmlprocess(data)
    num = len(content)
    worddict = {}
    stopwords = Stopwords()
    # print stopwords[:10]
    for sent in content:
        words = sent.strip().split(' ')
        for w in words:
            # print w.split('/')[0]
            if w.split('/')[0] in stopwords:
                continue
            # print w.split('/')[0]
            if not worddict.has_key(w):
                worddict[w] = {'idf': 0, 'tf': 1}
            else:
                worddict[w]['tf'] += 1
        for key in worddict:
            if key in words:
                worddict[key]['idf'] += 1

    return num, worddict

if __name__ == '__main__':
    fx = open('CfgCorpus.xml').read()
    print type(fx)
    #dom = xml.dom.minidom.parse(fx)
    #root = dom.documentElement
    #segs = root.getElementsByTagName("Question")
    # print len(segs)
    # for seg in segs:
    #	print seg.getElementsByTagName('FinalSeg')[0].childNodes[0].data
