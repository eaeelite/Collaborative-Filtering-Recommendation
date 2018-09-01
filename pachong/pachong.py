# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 13:34:07 2018

@author: liuyi_000
"""

import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
from collections import defaultdict

def get_links(url):
    responce=requests.get(url)#请求目标网站
    soup=BeautifulSoup(responce.text,'lxml')#解析网页源代码
    links_div=soup.find_all('div',class_='pic-panel')
    links=[div.a.get('href') for div in links_div]
    return links


def get_url(url):
    responce=requests.get(url)
    soup=BeautifulSoup(responce.text,'lxml')
    return soup
def get_house_info(house_url):
    house_soup=get_url(house_url)
    price=house_soup.find('span',class_='total').text.encode('utf8')
    unit=house_soup.find('span',class_='unit').text.encode('utf8')
    aaa=house_soup.find_all('p')
    area=aaa[0].text[3:].encode('utf8')
    huxing=aaa[1].text[5:11].encode('utf8')
    floor=aaa[2].text[3:].encode('utf8')
    direct=aaa[3].text[5:].encode('utf8')
    subway=aaa[4].text[3:].encode('utf8')
    community=aaa[5].text[3:].encode('utf8')
    loca=aaa[6].text[3:].encode('utf8')
    createtime=aaa[7].text[3:].encode('utf8')
    agent=house_soup.find('a',class_='name LOGCLICK')
    agent_name=agent.text.encode('utf8')
    agent_id=agent.get('data-el')
##################################
#特别注意：.text得到的文本是unicode类型，需要.encode('utf8')转换为str类型才可以使用
    info={
          u'价格':price,
          u'单位':unit,
          u'面积':area,
          u'户型':huxing,
          u'楼层':floor,
          u'朝向':direct,
          u'地铁':subway,
          u'小区':community,
          u'位置':loca,
          u'创建时间':createtime,
          u'经纪人名字':agent_name,
          u'经纪人id':agent_id      
          }
    info_list=[price,unit,area,huxing,floor,direct,subway,community,loca,
               createtime,agent_name,agent_id]
#    print info_list
    return info_list
    

if __name__ == "__main__": 
    
    url='https://bj.lianjia.com/zufang/'
    get_links(url)
    
#    house_url=get_links(url)[0]
#    info1=get_house_info(house_url)
    
    i=0
    info111=defaultdict()
    for link in get_links(url)[:10]:
        time.sleep(2)
        get_house_info(link)
        info111[i]=get_house_info(link)
        print(info111[i])
        i=i+1
    
    db=MySQLdb.connect('localhost','root','c5b4a3001','test',charset='utf8')
    #指定连接的cursor对象，由cursor对象执行SQL查询并获取结果
    cursor=db.cursor()  
    #不用指定key，defaultdict中包含默认的key
    sql_values,sql=defaultdict(),defaultdict()
    for i in range(10):
        values="'{}',"*11+"'{}'"  
        sql_values[i]=values.format(info111[i][0],info111[i][1]
                                   ,info111[i][2],info111[i][3]
                                   ,info111[i][4],info111[i][5]
                                   ,info111[i][6],info111[i][7]
                                   ,info111[i][8],info111[i][9]
                                   ,info111[i][10],info111[i][11])
    
        #values（）内部一定要搞成是纯文本的形式 format是很好的方式
        sql[i]="""insert into house(price,unit,area,huxing,floor,direct,subway
        ,community,loca,createtime,agent_name,agent_id) 
        values({})""".format(sql_values[i])
        cursor.execute(sql[i])    
        #执行操作后强行提交，才会更新数据库
        db.commit()  
    
    cursor.close()
    db.close()











