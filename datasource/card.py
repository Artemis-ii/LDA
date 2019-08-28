# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:09:40 2018

@author: Administrator
"""
import requests
from lxml import etree
import re
import xlwt



f = xlwt.Workbook() #创建工作簿
sheet1 = f.add_sheet(u'sheet1') #创建sheet
dlist = ['title', 'pic','text','content', 'from', 'date']
for i in range(len(dlist)):
   sheet1.write(0,i,dlist[i])	

counts=1


def jx(url):
    global counts
    #url="http://tieba.baidu.com/p/5722219880"
    r = requests.get(url)
    r.encoding='utf-8'
    s = r.text
    selector = etree.HTML(s)
    
    
    who =""
    count=1
    title = selector.xpath('//*[@class="core_title core_title_theme_bright"]/h1/text()')
    title = ''.join(title)
    pic = "kong"
    text=""
    context =""
    froms = "来源百度贴吧"
    date="2018-10-17 14:35"
    content = selector.xpath('//*[@class="l_post j_l_post l_post_bright  "]')
    #print("title:"+title)
    for i in content:
         kk = i.xpath('.//a[@class="p_author_name j_user_card"]/text()')
         kkk =  ''.join(kk)
         
         if count==1:
             who=kkk
             count = 2
         if who==kkk:
             ii = i.xpath('.//div[@class="d_post_content j_d_post_content  clearfix"]')
             kkkk =ii[0].xpath('string(.)')
             text = text+kkkk
             context = context+kkkk
             it = ''.join(ii[0].xpath('img/@src'))
             if "imgsrc"  in it:
                pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配模式
        
                url = re.findall(pattern,it)
                for i in url:
                    if i is not None:
                        ii = i.split("http")
                        for k in ii:
                            if "static" not  in k  and len(k)>10:

                                context = context+"sssshttp"+k+"ssss"
                                if pic =='kong':
                                    pic = "http"+k
    sheet1.write(counts,0,title)
    sheet1.write(counts,1,pic)	
    sheet1.write(counts,2,text)	
    sheet1.write(counts,3,context)
    sheet1.write(counts,4,froms)	
    sheet1.write(counts,5,date)
    counts = counts+1


for imun in range(4000,4500,50): 
    url="http://tieba.baidu.com/f?kw=%E7%BE%8E%E9%A3%9F&ie=utf-8&pn="+str(imun)
    #url="http://tieba.baidu.com/f?kw=meishi"
    r = requests.get(url)
    r.encoding='utf-8'
    s = r.text
    selector = etree.HTML(s)
    title = selector.xpath('//*[@class="threadlist_title pull_left j_th_tit "]')
    for  i in title:
        href = i.xpath('a/@href')
        #name = i.xpath('a/text()')
        href = 'http://tieba.baidu.com'+''.join(href)
        print(href)
        #print(''.join(name))
        #print("*"*30)
        jx(href)
f.save('cartdata14.xls')
    
    


















#获取帖子列表
'''
title = selector.xpath('//*[@class="threadlist_title pull_left j_th_tit "]')
for  i in title:
    href = i.xpath('a/@href')
    name = i.xpath('a/text()')
    print('http://tieba.baidu.com'+''.join(href))
    print(''.join(name))
    print("*"*30)
'''

#content = selector.xpath('//*[@class="d_post_content j_d_post_content  clearfix"]')
#content = content[0].xpath('string(.)')
#content =  ''.join(content)
#print(content)


#获取某一个帖子
'''
title = selector.xpath('//*[@class="core_title core_title_theme_bright"]/h1/text()')
title = ''.join(title)


content = selector.xpath('//*[@class="d_post_content j_d_post_content  clearfix"]')
print("title:"+title)
for i in content:
     #kk = i.xpath('//*[@id="post_content_95091918657"]')
     #kkk =  ''.join(kk)
     
     
     
     kkk =i.xpath('string(.)')
     print(kkk)
     
     it = ''.join(i.xpath('img/@src'))
     if "imgsrc"  in it:
        """
        slist = it.split('.jpg')
        for i in slist:
           if "imgsrc"  in i:
               print(i)
        """
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配模式

        url = re.findall(pattern,it)
        for i in url:
            if i is not None:
                ii = i.split("http")
                for k in ii:
                    if "static" not  in k  and len(k)>10:
                        print("|")
                        print("http"+k)
     
     print("*"*30)

'''
