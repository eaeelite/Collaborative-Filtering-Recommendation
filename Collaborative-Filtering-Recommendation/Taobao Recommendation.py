# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 13:18:18 2018

@author: liuyi_000
"""
'''
列名称	说明
用户ID	整数类型，序列化后的用户ID
商品ID	整数类型，序列化后的商品ID
商品类目ID	整数类型，序列化后的商品所属类目ID
行为类型	字符串，枚举类型，包括('pv', 'buy', 'cart', 'fav')
时间戳	行为发生的时间戳
'''

import pandas as pd
import numpy as np
import math
import operator
from collections import defaultdict #可以直接使用下标访问二维字典不存在的元素

def get_user_to_goods_unique(train100):
    a={}
    for i in range(len(train100)):
        if train100.ix[i,0] not in a.keys():
            a[train100.ix[i,0]]=[]
            a[train100.ix[i,0]].append(train100.ix[i,1])
            temp=train100.ix[i,0]
        else:
            if train100.ix[i,1] not in a[temp]:
                a[temp].append(train100.ix[i,1])
            if (i%10000)==0:
                print(i)
    return a
       
def cal_corated_users(train):
    C = defaultdict(defaultdict) 
    N = defaultdict(defaultdict) 
    m=0
    for u, items in train.items():
        for i in items:
            if i not in N.keys(): 
                N[i] = 0
            N[i] += 1
            for j in items:
                if i == j:
                   continue
                if j not in C[i].keys(): 
                    C[i][j] = 0
                C[i][j] += 1
            m+=1
            if (m%1000)==0:
                print(m)
    return C,N

def cal_matrix_W():
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j]) 
    return W

def get_user_to_goods_multi(train100):
    a={}
    for i in range(len(train100)):
        if train100.ix[i,0] not in a.keys():
            a[train100.ix[i,0]]={}
            a[train100.ix[i,0]][train100.ix[i,1]]=1
            temp=train100.ix[i,0]
        else:
            if train100.ix[i,1] not in a[train100.ix[i,0]].keys():
                a[temp][train100.ix[i,1]]=1
            else:
                a[temp][train100.ix[i,1]]+=1                  
            
            if (i%10000)==0:
                print(i)
    return a

def recommend(test, user_id, W, K):
    j_old=[]
    rank = dict()
    ru = test[user_id] #用户数据，表示某物品及其兴趣度
    for i, pi in ru.items(): #i表示用户已拥有的物品id，pi表示其兴趣度
        #j表示相似度为前K个物品的id，wj表示物品i和物品j的相似度
        print(i)
        for j, wj in sorted(W[i].items(),key = operator.itemgetter(1))[0:K]:
            if j in ru: #如果用户已经有了物品j，则不再推荐
                continue
            else:
                if(j not in j_old): 
                    rank[j]=0
                    j_old.append(j)
            rank[j]=rank[j]+pi*wj
    return rank

if __name__ == "__main__": 
    
    data_raw1=pd.read_csv('C:/Users/liuyi_000/.spyder/UserBehavior_00.csv',header=None)
    data_raw2=pd.read_csv('C:/Users/liuyi_000/.spyder/UserBehavior_01.csv',header=None)
    data_raw=pd.concat([data_raw1,data_raw2])
    data_raw.columns=['userid','goodsid','goodscat','beh','time']
    data_raw=data_raw.reset_index()
    del data_raw['index']

    train=data_raw[['userid','goodscat']].head(100000)
    train100=train.head(90000)
    
    test100=train.ix[90001:]
    test100=test100.reset_index()
    del test100['index']

    train100dict=get_user_to_goods_unique(train100)
    C,N=cal_corated_users(train100dict)

    W = defaultdict(defaultdict)
    W=cal_matrix_W()

    testtest=get_user_to_goods_multi(test100)
        
    user_id=100215
    ru={922588:3,284968:2,982926:2,2031969:4,2520377:5}
    test={user_id:ru}

    rank=recommend(testtest, 1003947, W, 233)
       
    sorted(rank.items(),key = operator.itemgetter(1),reverse=True)[:50]

