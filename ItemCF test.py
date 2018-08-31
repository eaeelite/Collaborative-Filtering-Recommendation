# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 17:47:20 2018

@author: liuyi_000
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 13:18:18 2018

@author: liuyi_000
"""

import pandas as pd
import numpy as np
import math
import operator
from collections import defaultdict #可以直接使用下标访问二维字典不存在的元素

def cal_corated_users(train):
    C = defaultdict(defaultdict) #不同用户共同喜欢物品的组合的分类与个数
    N = defaultdict(defaultdict) #选择某款商品的用户个数
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
            W[i][j] = cij / math.sqrt(N[i] * N[j]) #构造余弦相似度矩阵W
    return W
     

if __name__ == "__main__":   
      
    ###去除每位用户选择重复的商品
    ###大写字母代表用户 小写字母代表商品
    itemcf={'A':['a','b','d']
           ,'B':['b','c','e']
           ,'C':['c','d']
           ,'D':['b','c','d']
           ,'E':['a','d']} 
    C,N=cal_corated_users(itemcf)
    W = defaultdict(defaultdict)
    W=cal_matrix_W()
    
    user_id=123
    fav={'a':1,'b':2,'c':2}
    test={user_id:fav}
    
    j_old=[]
    rank = dict()
    ru = test[user_id] #用户数据，表示某物品及其兴趣度
    for i, pi in ru.items(): #i表示用户已拥有的物品id，pi表示其兴趣度
        #j表示相似度为前K个物品的id，wj表示物品i和物品j的相似度
        print(i)
        for j, wj in sorted(W[i].items(),key = operator.itemgetter(1))[0:5]:
            if j in ru: #如果用户已经有了物品j，则不再推荐
                continue
            else:
                if(j not in j_old): 
                    rank[j]=0
                    j_old.append(j)
            rank[j]=rank[j]+pi*wj
    print(rank)#   
    
    
    
    
    
    
