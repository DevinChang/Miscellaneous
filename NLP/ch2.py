# -*- coding: utf-8 -*-



import nltk
#from nltk.book import *
from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.util import bigrams
from nltk.corpus import stopwords


emma = gutenberg.words('austen-emma.txt')


#for fileid in gutenberg.fileids():
#    num_chars = len(gutenberg.raw(fileid))
#    num_words = len(gutenberg.words(fileid))
#    num_sents = len(gutenberg.sents(fileid))
#    num_vocab = len(set([w.lower() for w in gutenberg.words(fileid)]))
#    print (int(num_chars / num_words), int(num_words / num_sents), int(num_words / num_vocab), fileid)

#比较不同文体情态动词的用法
#1.产生特定文体的计数
#news_text = brown.words(categories = 'news')
#fdist = nltk.FreqDist([w.lower() for w in news_text])
#modals = ['can', 'could', 'may', 'might', 'must', 'will']
#for m in modals:
#    print(m + ':', fdist[m])
#
##2
#cfd = nltk.ConditionalFreqDist(
#    (genre, word)
#    for genre in brown.categories()
#    for word in brown.words(categories = genre)
#)
#
#genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
#modals = ['can', 'could', 'may', 'might', 'must', 'will']
#cfd.tabulate(conditions = genres, samples = modals)
#
#
##条件概率分布
#cfd = nltk.ConditionFreqDist(
#    (target, fileid[:4])
#    for fileid in inaugural.fileids()
#    for w in inaugural.words(fileid)
#    for target in ['america', 'citizen']
#    if w.lower().startswith(target)
#)
#
#cfd.plot()

#raw words, sents的区别
#raw = gutenberg.raw("burgess-busterbrown.txt")
#print(raw[1:20])
#words = gutenberg.words("burgess-busterbrown.txt")
#print(words[1:20])
#sents = gutenberg.sents("burgess-busterbrown.txt")
#print(sents[1:20])

#def generate_model(cfdist, word, num = 15):
#    for i in range(num):
#        print(word)
#        word = cfdist[word].max()
#
#
#text = nltk.corpus.genesis.words('english-kjv.txt')
#bigrams = nltk.bigrams(text)
#cfd = nltk.ConditionalFreqDist(bigrams)
#
#print(cfd['living'])
#generate_model(cfd, 'living')
#
#
#def lexical_diversity(my_text_data):
#    word_count = len(my_text_data)
#    vocab_size = len(set(my_text_data))
#    diversity_score = word_count / vocab_size
#    return diversity_score
#
##单词变复数形式
#def plural(word):
#    if word.endswith('y'):
#        return word[:-1] + 'ies'
#    elif word[:-1] in 'sx' or word[-2:] in ['sh', 'ch']:
#        return word + 'es'
#    elif word.endswith('an'):
#        return word[:-2] + 'en'
#    else:
#        return word + 's'
#
##2.3过滤文本
#def unusual_words(text):
#    text_vocab = set(w.lower() for w in text if w.isalpha())
#    english_vacab = set(w.lower() for w in nltk.corpus.words.words())
#    unusual = text_vocab.difference(english_vacab)
#    return sorted(unusual)

#计算没有在停用表中的词的比例
#error: 会一直执行，陷入死循环
#def content_fraction(text):
#    stopwords = nltk.corpus.stopwords.words('english')
#    content = [w for w in text if w.lower() not in stopwords]
#    return len(content) / len(text)
'''
#名字的统计
names = nltk.corpus.names
print(names.fileids())
male_names = names.words('male.txt')
female_names = names.words('female.txt')
print([w for w in male_names if w in female_names])

cfd = nltk.ConditionalFreqDist(
            (fileid, name[-1])
            for fileid in names.fileids()
            for name in names.words(fileid)
)
cfd.plot()
'''

#发音的词典
entries = nltk.corpus.cmudict.entries()
for entry in entries[39943 : 39951] : 
    print(entry)


for word, pron in entries:
    if len(pron) == 3:
        ph1, ph2, ph3 = pron
        if ph1 == 'P' and ph3 == 'T':
            print(word, ph2)





def stress(pron):
    return [char for phone in pron for char in phone if char.isdigit()]

letter = [w for w, pron in entries if stress(pron) == ['0', '1', '0', '2', '0']]
#print(letter)


p3 = [(pron[0] + '-' + pron[2], word)
        for (word, pron) in entries
        if pron[0] == 'P' and len(pron) == 3]

cfd = nltk.ConditionalFreqDist(p3)
for template in cfd.conditions():
    if len(cfd[template]) > 10:
        words = cfd[template].keys()
        wordlist = ' '.join(words)
        print(template, wordlist[:70] + "...")


