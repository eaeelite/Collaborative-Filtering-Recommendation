# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 20:33:13 2018

@author: liuyi_000
"""

import pandas as pd 
'''
data=pd.read_csv('air_data.csv')
explore=data.describe(percentiles=[],include='all').T

explore['null']=len(data)-explore['count']
explore=explore[['null','max','min']]
resultfile='explore.xls'
explore.to_excel(resultfile)
print(len(data))
data=data[data['SUM_YR_1'].notnull()*data['SUM_YR_2'].notnull()]
index1=data['SUM_YR_1']!=0
index2=data['SUM_YR_2']!=0
index3=(data['SEG_KM_SUM']==0)&(data['avg_discount']==0)
data=data[index1|index2|index3]
'''

data=pd.read_excel('zscoreddata.xls')
data=(data-data.mean(axis=0))/data.std(axis=0)
data.columns=[i for i in data.columns]
#data.to_excel('zscoreddata1.xls',index=False)

data1=data

from sklearn.cluster import KMeans
from collections import Counter

k=5
kmodel=KMeans(n_clusters=k)
kmodel.fit(data1)

centers=pd.DataFrame(kmodel.cluster_centers_)
labels=kmodel.labels_
count=dict(Counter(labels))
res=pd.DataFrame(count,index=['count']).T

results=pd.concat([res,centers],axis=1)


