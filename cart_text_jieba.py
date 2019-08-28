# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 15:41:02 2018

@author: 月神少女
"""

import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs,sys
from string import punctuation

from text_parse import TEXT_parse

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

class CART_text_jieba():
    def __init__(self,txt_file,jieba_txt):
        self.txt_file = txt_file
        self.jieba_txt = jieba_txt
    def jieba(self):        
        # 定义要删除的标点等字符
        add_punc='，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'
        all_punc=punctuation+add_punc
        f=codecs.open(self.txt_file,'r',encoding="utf8")
        target = codecs.open(self.jieba_txt, 'w',encoding="utf8")
        print ('open files')
        line_num=1
        line = f.readline()
        while line:
            print('---- processing ', line_num, ' article----------------')
        
            line_seg = " ".join(jieba.cut(line.replace("\n","")))
            # 移除标点等需要删除的符号
            testline=line_seg.split(' ')
            te2=[]
            for i in testline:
                te2.append(i)
                if i in all_punc:
                    te2.remove(i)
            # 返回的te2是个list，转换为string后少了空格，因此需要再次分词
        	# 第二次在仅汉字的基础上再次进行分词
            line_seg2 = " ".join(jieba.cut(''.join(te2)))
            target.writelines(line_seg2)
            line_num = line_num + 1
            line = f.readline()
        f.close()
        target.close()
        
'''        
if __name__=="__main__":
  dire="datasource/cartdata"
  txt="data/cart_text.txt"
  cut_txt = "data/cart_text_cut.txt"
  stopword = "data/stopword.txt"
  text = TEXT_parse(directory=dire,txt_file=txt)
  text.parse()
  text_jieba = CART_text_jieba(txt_file=txt,jieba_txt=cut_txt)
  text_jieba.jieba()
'''

        
        
