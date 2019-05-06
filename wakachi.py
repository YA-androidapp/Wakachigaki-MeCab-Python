#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
# Required:
#  $ sudo apt install -y mecab libmecab-dev mecab-ipadic-utf8
#  $ pip install mecab-python3


import datetime
import MeCab
import os
import sys


nowts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
scrpath = os.path.abspath(os.path.dirname(__file__))
os.chdir(scrpath)


input_file  = 'input.txt'
output_file = 'output_' + nowts + '.txt'

wakachiSep = " ";
labelSep = " ";


def formFilter(res):
    pos = (res.feature.split(','))[0]
    basic = (res.feature.split(','))[6]
    surface = res.surface
    if '' == surface:
        return ''

    w = basic if ('*' != basic) else surface
    if '名詞' == pos:
        return w
    elif '動詞' == pos:
        return w
    elif '形容詞' == pos:
        return w
    else:
        return ''


def wakachi(str):
    result = []

    mt = MeCab.Tagger('-d ./dic')
    mt.parse('')
    tok = mt.parseToNode(str)
    while tok:
        res = formFilter(tok)
        if len(res) > 0:
            result.append(res)
        tok = tok.next
    return wakachiSep.join(result)


def main():
    if os.path.exists(input_file) and os.path.isfile(input_file):
        fi = open(input_file)
        line = fi.readline().rstrip('\r\n')
        with open(output_file, 'a') as fo:
            while line:
                rowParts = line.split(labelSep)
                strs = [];
                tags = [];
                for rowPart in rowParts:
                    if (rowPart.startswith('__label__')):
                        tags.append(rowPart)
                    else:
                        strs.append(rowPart)
                print( labelSep.join(tags) + labelSep + (wakachi((labelSep.join(strs)).strip())) , file=fo)
                line = fi.readline()
        fi.close

if __name__ == '__main__':
    main()

