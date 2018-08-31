# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 21:18:36 2018

@author: liuyi_000
"""

import pandas as pd
from random import shuffle

data=pd.read_excel('C:\Users\liuyi_000\.spyder\model.xls')
data=data.as_matrix()
shuffle(data)

p=0.8
train=data[:int(len(data)*p),:]
test=data[int(len(data)*p):,:]
 
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

tree=DecisionTreeClassifier(criterion='entropy')
tree.fit(train[:,:3],train[:,3])

joblib.dump(tree,'tree.pkl')


def cm_plot(y, yp):
  
  from sklearn.metrics import confusion_matrix #µ¼Èë»ìÏý¾ØÕóº¯Êý

  cm = confusion_matrix(y, yp) #»ìÏý¾ØÕó
  
  import matplotlib.pyplot as plt #µ¼Èë×÷Í¼¿â
  plt.matshow(cm, cmap=plt.cm.Greens) #»­»ìÏý¾ØÕóÍ¼£¬ÅäÉ«·ç¸ñÊ¹ÓÃcm.Greens£¬¸ü¶à·ç¸ñÇë²Î¿¼¹ÙÍø¡£
  plt.colorbar() #ÑÕÉ«±êÇ©
  
  for x in range(len(cm)): #Êý¾Ý±êÇ©
    for y in range(len(cm)):
      plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
  
  plt.ylabel('True label') #×ø±êÖá±êÇ©
  plt.xlabel('Predicted label') #×ø±êÖá±êÇ©
  return plt
cm_plot(train[:,3], tree.predict(train[:,:3]))

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
predict_result=tree.predict(test[:,:3]).reshape(len(test))
fpr,tpr,thresholds=roc_curve(test[:,3],predict_result,pos_label=1)
plt.plot(fpr,tpr)







