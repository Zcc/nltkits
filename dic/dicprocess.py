# ! /usr/bin/env python
# coding=utf-8

def aliases():
    dic = open('aliases.dic', 'w')
    for line in open('aliases.txt'):
        words = line.strip().split('|')
        words = set(words)
        dic.write('|'.join(words)+'\n')
    dic.close()

def hitsynonymy():
    dic = open('synonymy.dic','w')
    for line in open('hitsynonymy.txt'):
        words = line.strip().split(' ')
        if '=' in words[0]:
            dic.write('|'.join(words[1:])+'\n')
    dic.close()

if __name__ == '__main__':
    aliases()
    hitsynonymy()
