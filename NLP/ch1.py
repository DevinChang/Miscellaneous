# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.book import *

#统计文本在文章中占比
def lexical_diversity(text):
    return len(text) / len(set(text))


#百分比
def percentate(count, total):
    return 100 * count / total

#频率分布
fdist1 = FreqDist(text1)
vocalbulary1 = fdist1.keys()

#筛选出特定的文本
V = set(text1)
long_word = [w for w in V if len(w) > 15]

#词语搭配
text4.collocations()


#超过7个字符出现次数超过7次
fdist5 = FreqDist(text5)
print(sorted([w for w in set(text5) if len(w) > 7 and fdist5[w] > 7]))
print(sorted(long_word))