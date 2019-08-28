# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 15:20:33 2018

@author: 月神少女
"""

import xlrd
import re

class TEXT_parse():
    def __init__(self,directory,txt_file):
        self.directory = directory
        self.txt_file = txt_file
    def parse(self):        
        for i in range(1,2):
            xls_file = xlrd.open_workbook(self.directory + str(i) + ".xls")
            txt_file = open(self.txt_file,'a+', encoding = 'utf-8')
            xls_sheet = xls_file.sheets()[0]
            col_value_1 = xls_sheet.col_values(0) #读取title字段
            col_value_2 = xls_sheet.col_values(2) #读取text字段
            
            for i in range(1,len(col_value_1)):
                #去除title和text中所有的空格，特殊字符中文字符等和所有的数字的英文
                title = re.sub(r'\s|\W|[a-zA-Z0-9]', '', col_value_1[i]) 
                text = re.sub(r'\s|\W|[a-zA-Z0-9]', '', col_value_2[i])
                txt_file.write(title + text + '\n')
                print(i)
            txt_file.close()
            

        