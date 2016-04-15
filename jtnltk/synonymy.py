#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

reload(sys)

sys.setdefaultencoding("utf-8")


def get_synonymy(wordlist, dicname):
    index, lines = aliases_dic(dicname)
    alifile = open('static/tmp/' + dicname + '.txt', 'w')
    aliases = []
    for word in wordlist:
        word = word.strip()
        # print word
        st = word + ' '
        if index.has_key(word):
            for inx in index[word]:
                st += ' '.join([w for w in lines[inx] if w != word]) + ' '
        st = st.strip() + '\n'
        alifile.write(st)

        aliases.append(st.strip().split(' '))
    # print len(aliases)
    alifile.close()
    return aliases


def get_wiki_synonymy(wordlist):
    return get_synonymy(wordlist, 'aliases')


def get_hit_synonymy(wordlist):
    return get_synonymy(wordlist, 'synonymy')


def aliases_dic(dicname):
    lines = []
    index = {}
    tot = 0
    filename = 'dic/' + dicname + '.dic'
    for line in open(filename):
        words = line.strip().split('|')
        lines.append(words)
        for word in words:
            if index.has_key(word):
                index[word].append(tot)
            else:
                index[word] = [tot]
        tot += 1
    return index, lines


if __name__ == '__main__':
    aliases_dic()
