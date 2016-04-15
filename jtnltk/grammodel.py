#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd
import sys
import os
import jieba
import jieba.analyse
from gensim import corpora, models, similarities
from numpy import *
from operator import itemgetter

reload(sys)
sys.setdefaultencoding('utf-8')


def Stopwords():
    return [w.strip() for w in open('dic/stopwords.dic').readlines()]


def loadfile(filename):
    print "loading file......"
    xlx = xlrd.open_workbook(filename)

    return xlx


def getcolvalues(xlx, num):
    table = xlx.sheets()[0]
    return table.col_values(num)


def segment(sentence):
    stopwords = Stopwords()
    return [w for w in jieba.cut(str(sentence.strip())) if w not in stopwords]


def segmentlist(sentencelist):
    return [segment(w.strip()) for w in sentencelist]


def getDictionary(sentencelist):
    return corpora.Dictionary(segmentlist(sentencelist))


def getCorpus(sentencelist):
    return [getDictionary(sentencelist).doc2bow(t) for t in segmentlist(sentencelist)]


def getCorpus(dic, sentencelist):
    return [dic.doc2bow(t) for t in segmentlist(sentencelist)]


def getTfidf(corpus):
    return models.TfidfModel(corpus)


def tfidfTofile(tfidf, dictionary):
    idf = open('static/tmp/idf.txt', 'w')
    idfmap = tfidf.idfs
    #print type(idfmap)
    idfmap = sorted(idfmap.iteritems(), key=itemgetter(1), reverse=False)
    for t in idfmap:
        idf.write(str(dictionary[t[0]]) + '\t' + str(t[1]) + '\n')
    tfidf.save('static/tmp/tfidf.model')


def extract_tags(sentence, topn):
    return jieba.analyse.extract_tags(sentence, topK=topn, withWeight=False, allowPOS=())


def getNparry(tfidf, dicnum):
    nparry = zeros((len(tfidf), dicnum), dtype='float32')
    for i, doc in enumerate(tfidf):
        print i, doc
        for w in enumerate(doc):
            nparry[i, w[1][0]] = w[1][1]
    return nparry


def getsimilarity(corpus_tfidf, query_tfidf, topn):
    result = []
    for query in query_tfidf:
        re = {}
        for i, corpus in enumerate(corpus_tfidf):
            cos = getCos(query, corpus)
            re[i] = cos
        resort = sorted(re.iteritems(), key=itemgetter(1), reverse=True)[:topn]
        result.append(resort)
    return result


def getCos(vector1, vector2):
    v1s = sum([v[1] * v[1] for v in vector1]) ** 0.5
    v2s = sum([v[1] * v[1] for v in vector2]) ** 0.5
    v1v2 = 0
    i = 0
    for v1 in vector1:
        if i >= len(vector2): break
        if v1[0] == vector2[i][0]: v1v2 += v1[1] * vector2[i][1]
        if v1[0] < vector2[i][0]: continue
        i += 1
    return v1v2 / v1s * v2s


def traincorpus(sentencelist):
    dictionary = getDictionary(sentencelist)
    corpus = getCorpus(dictionary, sentencelist)
    tfidf = getTfidf(corpus)
    tfidfTofile(tfidf, dictionary)
    return tfidf


def loadtfidfmodel():
    print "loading model......"
    return models.TfidfModel.load('tfidf.model')

def train_tfidf(sentencelist):
    seg = segmentlist(sentencelist)
    dictionary = corpora.Dictionary(seg)
    corpus = [dictionary.doc2bow(t) for t in seg]
    tfidf = models.TfidfModel(corpus)
    tfidfTofile(tfidf, dictionary)
    return tfidf

def train_lda(sentencelist,topicnum=20):
    seg = segmentlist(sentencelist)
    dictionary = corpora.Dictionary(seg)
    corpus = [dictionary.doc2bow(t) for t in seg]
    tfidf = models.TfidfModel(corpus)
    tfidfTofile(tfidf, dictionary)
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus_tfidf, num_topics=topicnum)
    topics = lda.print_topics(topicnum, 10)
    flda = open('static/tmp/lda.txt','w')
    for ts in topics:
        topic = ts.split('+')
        s = ''
        for t in topic:
            tid = t.strip().split('*')[1]
            s += dictionary.get(int(tid))+' '
        flda.write(s.strip()+'\n')
            #print dictionary.get(int(tid))
    return lda

def train(sentencelist):
    print 'segmenting....'
    seg = segmentlist(sentencelist)
    dictionary = corpora.Dictionary(seg)
    print 'saving dictionary....'
    dictionary.save('dictionary.bin')
    dictionary.save_as_text('dictionary.dic')
    corpus = [dictionary.doc2bow(t) for t in seg]
    print 'training tfidf model....'
    tfidf = models.TfidfModel(corpus)
    print 'saving tfidf model....'
    tfidf.save('tfidf.model')
    corpus_tfidf = tfidf[corpus]
    print 'training LSI model....'
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=20)
    print 'saving LSI model....'
    lsi.save('lsi.model')
    print 'training LDA model....'
    lda = models.LdaModel(corpus_tfidf, num_topics=40)
    print 'saving LDA model....'
    lda.save('lda.model')
    print 'train sucessfully....'


def TopnSimilarity(model, corpus, query):
    index = similarities.MatrixSimilarity(model[corpus])
    query = model[bow]
    sims = index[query]
    for s in sims:
        sort_sims = sorted(enumerate(s), key=lambda item: -item[1])
        for x in sort_sims[:10]:
            print sentencelist[x[0]], x[1]
        print


def doc2vector(sentencelist):
    sentences = []
    for i in xrange(len(sentencelist)):
        lab = "SENT_" + str(i)
        sentence = models.doc2vec.TaggedDocument(sentencelist[i], tags=[lab])
        sentences.append(sentence)
    doc2vecmodel = models.Doc2Vec(sentences, size=100, window=5, min_count=0, dm=1)
    doc2vecmodel.build_vocab(sentences)
    doc2vecmodel.init_sims()

    return doc2vecmodel


if __name__ == '__main__':
    # sentencelist = ['今天天气不错', '后天天气也不错','明天天气怎样？']
    #xlx = loadfile('finance.xlsx')
    #sentencelist = getcolvalues(xlx, 5)
    #train(sentencelist)
    # #print len(sentencelist)
    #dictionary = getDictionary(sentencelist)
    # # dictionary.save('')
    # #dictionary.save_as_text('dictionary.text')
    # #dict = corpora.Dictionary.load_from_text('dictionary.text')
    dictionary = corpora.Dictionary.load('dictionary.bin')
    # #dicnum = len(dictionary)
    #corpus = getCorpus(dictionary, sentencelist)
    #tfidf = getTfidf(corpus)
    tfidf = loadtfidfmodel()
    tfidfTofile(tfidf,dictionary)

    #query = ['什么是贴现？', '发起协议是什么？', '网上开户安全吗？', '我的账户被冻结了，我可以不销户自己开户吗？','公司在哪？','公司地址在哪？']
    # d2v = doc2vector(segmentlist(sentencelist))
    # for i in d2v.most_similar(u'开户'):
    #     print i[0],i[1]
    #query_bow = getCorpus(dictionary, query)
    #corpus_tfidf = tfidf[corpus]
    # query_tfidf = tfidf[query_bow]
    # for s in getsimilarity(corpus_tfidf,query_tfidf,5):
    #     for x in s:
    #         print sentencelist[x[0]], x[1]
    #     print
    # #
    # lsi = models.LsiModel.load('lsi.model')
    # index = similarities.MatrixSimilarity(lsi[corpus])
    # querylsi = lsi[query_bow]
    # sims = index[querylsi]
    # for s in sims:
    #     sort_sims = sorted(enumerate(s), key=lambda item: -item[1])
    #     for x in sort_sims[:5]:
    #         print sentencelist[x[0]],x[1]
    #     print

    # tfidf = loadtfidfmodel()
    # index = similarities.MatrixSimilarity(tfidf[corpus])
    # querylsi = tfidf[query_bow]
    # sims = index[querylsi]
    # for s in sims:
    #     sort_sims = sorted(enumerate(s), key=lambda item: -item[1])
    #     for x in sort_sims[:5]:
    #         print sentencelist[x[0]], x[1]
    #     print

    lda = models.LdaModel.load('lda.model')
    #print lda.print_topics(2, 10)
    topics = lda.print_topics(40,1)
    for ts in topics:
        topic = ts.split('+')
        for t in topic:
            tid = t.strip().split('*')[1]
            print dictionary.get(int(tid))

    # query_lda = lda[query_tfidf]
    # for doc in query_lda:
    #     print doc
    # index = similarities.MatrixSimilarity(lda[corpus])
    # querylsi = lda[query_bow]
    # sims = index[querylsi]
    # for s in sims:
    #     sort_sims = sorted(enumerate(s), key=lambda item: -item[1])
    #     for x in sort_sims[:10]:
    #         print sentencelist[x[0]], x[1]
    #     print
        # querytfidf = tfidf[getCorpus(dictionary,query)]
        # for x in getsimilarity(corpus_tfidf,querytfidf,5):
        #     for s in x:
        #         print s[0],sentencelist[s[0]],s[1]
        #     print
