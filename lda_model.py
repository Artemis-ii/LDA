# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 16:29:00 2019

@author: Yoi
"""

import numpy as np
import lda
import lda.datasets
import jieba
import codecs

from text_parse import TEXT_parse 
from cart_text_jieba import CART_text_jieba

class LDA_model():
  def __init__(self, topics=2):
    self.n_topic = topics
    self.corpus = None
    self.vocab = None
    self.ppCountMatrix = None
    self.stop_words = [u'，', u'。', u'、', u'（', u'）', u'·', u'！', u' ', u'：', u'“', u'”', u'\n']
    self.model = None
  def loadCorpusFromFile(self, fn,stop_words):
    # 中文分词
    f = open(fn, 'r',encoding = 'utf-8')
    text = f.readlines()
    text = r' '.join(text)
    seg_generator = jieba.cut(text)
    seg_list = [i for i in seg_generator if i not in stop_words]
    #print(seg_list)
    seg_list = r' '.join(seg_list)
    # 切割统计所有出现的词纳入词典
    seglist = seg_list.split(" ")
    self.vocab = []
    for word in seglist:
      if (word != u' ' and word not in self.vocab):
        self.vocab.append(word)
    CountMatrix = []
    f.seek(0, 0)
    # 统计每个文档中出现的词频
    for line in f:
      # 置零
      count = np.zeros(len(self.vocab),dtype=np.int)
      text = line.strip()
      # 但还是要先分词
      seg_generator = jieba.cut(text)
      seg_list = [i for i in seg_generator if i not in stop_words]
      seg_list = r' '.join(seg_list)
      seglist = seg_list.split(" ")
      # 查询词典中的词出现的词频
      for word in seglist:
        if word in self.vocab:
          count[self.vocab.index(word)] += 1
      CountMatrix.append(count)
    f.close()
    #self.ppCountMatrix = (len(CountMatrix), len(self.vocab))
    self.ppCountMatrix = np.array(CountMatrix)
    print("load corpus from %s success!"%fn)
    
    #建立停用词
  def setStopWords(self, word_list):
    self.stop_words = word_list
    
    #生成模型
  def fitModel(self, n_iter = 1500, _alpha = 0.1, _eta = 0.01):
    self.model = lda.LDA(n_topics=self.n_topic, n_iter=n_iter, alpha=_alpha, eta= _eta, random_state= 1)
    self.model.fit(self.ppCountMatrix)
    
  def printTopic_Word(self, n_top_word = 8):
    for i, topic_dist in enumerate(self.model.topic_word_):
      topic_words = np.array(self.vocab)[np.argsort(topic_dist)][:-(n_top_word + 1):-1]
      print("Topic:" + str(i) + "\n")
      for word in topic_words:
        if word == "":
            continue
        print(word + " " + str(topic_dist[i]) + "\n")
      print("\n")
      
    # 生成词
  def saveVocabulary(self, fn):
    f = codecs.open(fn, 'w', 'utf-8')
    for word in self.vocab:
      f.write("%s\n"%word)
    f.close()
    
    #将 主题与词的对应写入 TXT文件
  def saveTopic_Words(self, fn, n_top_word = 10):
    if n_top_word==-1:
      n_top_word = len(self.vocab)
    f = codecs.open(fn, 'w', 'utf-8')
    for i, topic_dist in enumerate(self.model.topic_word_):
      topic_words = np.array(self.vocab)[np.argsort(topic_dist)][:-(n_top_word + 1):-1]
      f.write( "Topic:%d\n"%i)
      for word in topic_words:
        if word == "":
            continue
        f.write(word + " " + str(topic_dist[i]) + "\n")
      f.write("\n")
    f.close()
    
    #将 文档所属主题的概率写入TXT文件
  def saveDoc_Topic(self, fn):
    f = codecs.open(fn, 'w', 'utf-8')
    for i in range(len(self.ppCountMatrix)):
      f.write("Doc %d:((top topic:%s) topic distribution:%s)\n" % (i, self.model.doc_topic_[i].argmax(), self.model.doc_topic_[i]))
    f.close()
    
    #将 文档所属主题的结果写入TXT文件
  def saveDoc_Address(self, fn):
    f = codecs.open(fn, 'w', 'utf-8')
    for i in range(len(self.ppCountMatrix)):
      f.write("Doc %d:(top topic:%s)\n" % (i, self.model.doc_topic_[i].argmax()))
    f.close()
    
    
if __name__=="__main__":
    dire="datasource/cartdata"
    txt="data/cart_text.txt"
    cut_txt = "data/cart_text_cut.txt"
    stopword = "data/stopword.txt"
    text = TEXT_parse(directory=dire,txt_file=txt)
    text.parse()
    text_jieba = CART_text_jieba(txt_file=txt,jieba_txt=cut_txt)
    text_jieba.jieba()
    for i in range(5,20,2):
      num_topics = i
      _lda = LDA_model(topics=num_topics)
      file = open(stopword,encoding="utf-8")
      stop_words = [i.replace(u'\n','') for i in file.readlines() if i.startswith(u'\n')==False]
      #print(stop_words)
      _lda.setStopWords(stop_words)
      _lda.loadCorpusFromFile(cut_txt,stop_words)
      _lda.fitModel(n_iter=1500)
      _lda.printTopic_Word(n_top_word=10)
      _lda.saveVocabulary('data/result/vocab_' + str(num_topics) + '.txt')
      _lda.saveTopic_Words('data/result/topic_word_' + str(num_topics) + '.txt')
      _lda.saveDoc_Topic('data/result/doc_topic_' + str(num_topics) + '.txt')
      _lda.saveDoc_Address('data/result/doc_address_' + str(num_topics) + '.txt')
      
      '''
      ss="长话短说\n就哈哈哈哈"
      print(ss.replace(u'\n',''))
      print(ss.startswith(u'\n')==False)
      stop_words=["长话短说\n","长话短说\n","长话短说\n","长话短说\n","长话短说\n","我\n","在\n",]
      seg_generator=jieba.cut("我在做的重庆口味的水煮鱼，老家的重庆渝香辣婆婆水煮鱼都是改良过的")
      seg_list = [i for i in seg_generator if i not in stop_words]
      print(seg_list)
      '''
      
      
    
