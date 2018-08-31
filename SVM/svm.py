# -*- coding: utf-8 -*-
"""
Created on Sun Mar 04 21:49:04 2018

list是列表,可以通过索引查找数值，但是不能对整个列表进行数值运算
array是数组，也可以通过索引值查找数据，但是能对整个数组进行数值运算
@author: liuyi_000
"""
import random
import pandas as pd
from random import shuffle
from sklearn import svm,metrics
import numpy as np

data=pd.read_csv('moment.csv',sep='\t')

data1=data.as_matrix()
'''
random.shuffle(data1)
data_train=data1[:int(0.8*len(data1)),:]
data_test=data1[int(0.8*len(data1)):,:]
'''
data_train1=random.sample(data1,int(0.8*len(data1)))
data_test1=random.sample(data1,int(0.2*len(data1)))

data_train=np.array(data_train1)
data_test=np.array(data_test1)

x_train=data_train[:,2:]*30
y_train=data_train[:,0].astype(int)
x_test=data_test[:,2:]*30
y_test=data_test[:,0].astype(int)

model=svm.SVC()
model.fit(x_train,y_train)
import pickle
pickle.dump(model,open('svm111.model','wb'))

cm_train=metrics.confusion_matrix(y_train,model.predict(x_train))
cm_test=metrics.confusion_matrix(y_test,model.predict(x_test))

print cm_train,'\n''\n',cm_test






