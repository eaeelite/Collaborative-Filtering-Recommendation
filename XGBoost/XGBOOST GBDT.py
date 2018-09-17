# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 16:47:11 2018

@author: liuyi_000
"""
import matplotlib.pyplot as plt
import time
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

data_raw1=pd.read_csv('C:/Users/liuyi_000/.spyder/UserBehavior_00.csv',header=None)
data_raw2=pd.read_csv('C:/Users/liuyi_000/.spyder/UserBehavior_01.csv',header=None)
data_raw=pd.concat([data_raw1,data_raw2],axis=0,ignore_index=True)
data_raw.columns=['a','b','c','d','e']

user_count=data_raw.ix[:,0].unique()

data_raw=data_raw.sort_values(by='b')
item_count=data_raw.b.unique()

pv=data_raw[data_raw.d=='pv'].d.groupby(data_raw.b).count()
cart=data_raw[data_raw.d=='cart'].d.groupby(data_raw.b).count()
buy=data_raw[data_raw.d=='buy'].d.groupby(data_raw.b).count()
fav=data_raw[data_raw.d=='fav'].d.groupby(data_raw.b).count()
pv=pd.DataFrame(pv)
cart=pd.DataFrame(cart)
buy=pd.DataFrame(buy)
fav=pd.DataFrame(fav)
pv.columns=['pv']
cart.columns=['cart']
buy.columns=['buy']
fav.columns=['fav']

item=pd.DataFrame(item_count,index=item_count,columns=['itemname'])
item=item.join(buy)
item=item.join(cart)
item=item.join(fav)
item=item.join(pv)

item['pv/buy']=item.pv/item.buy
item['cart/buy']=item.cart/item.buy
item['fav/buy']=item.fav/item.buy
item['label']=item.buy/item.buy
item=item.fillna(0)

temp=item.sort_values(by='buy',ascending=False)
buy_count=temp[temp.buy==1]
item=temp.iloc[:130000,:]

x,y=item.iloc[:,2:5],item.iloc[:,-1]
data_dmatrix=xgb.DMatrix(data=x,label=y)
for i in range(10):
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=100)
    
    result=pd.DataFrame(index=['dt','rf','ada','gbdt','xgb']
                        ,columns=['AUC','Acc','Pre','Rec','time'])
    
    start=time.time()
    gbdt=DecisionTreeClassifier()
    gbdt.fit(x_train,y_train)
    pre_dt=gbdt.predict(x_test)
    cm = confusion_matrix(y_test,pre_dt)
    result.iloc[0,0]=metrics.roc_auc_score(y_test, pre_dt) 
    result.iloc[0,1]=metrics.accuracy_score(y_test, pre_dt)
    result.iloc[0,2]=metrics.precision_score(y_test, pre_dt)
    result.iloc[0,3]=metrics.recall_score(y_test, pre_dt)
    end=time.time()
    result.iloc[0,4]=end-start
    
    start=time.time()
    gbdt=RandomForestClassifier()
    gbdt.fit(x_train,y_train)
    pre_rf=gbdt.predict(x_test)
    cm = confusion_matrix(y_test,pre_rf)
    result.iloc[1,0]=metrics.roc_auc_score(y_test, pre_rf) 
    result.iloc[1,1]=metrics.accuracy_score(y_test, pre_rf)
    result.iloc[1,2]=metrics.precision_score(y_test, pre_rf)
    result.iloc[1,3]=metrics.recall_score(y_test, pre_rf)
    end=time.time()
    result.iloc[1,4]=end-start
    
    start=time.time()
    gbdt=AdaBoostClassifier()
    gbdt.fit(x_train,y_train)
    pre_ada=gbdt.predict(x_test)
    cm = confusion_matrix(y_test,pre_ada)
    result.iloc[2,0]=metrics.roc_auc_score(y_test, pre_ada) 
    result.iloc[2,1]=metrics.accuracy_score(y_test, pre_ada)
    result.iloc[2,2]=metrics.precision_score(y_test, pre_ada)
    result.iloc[2,3]=metrics.recall_score(y_test, pre_ada)
    end=time.time()
    result.iloc[2,4]=end-start
    
    start=time.time()
    gbdt=GradientBoostingClassifier()
    gbdt.fit(x_train,y_train)
    pre_gbdt=gbdt.predict(x_test)
    cm = confusion_matrix(y_test,pre_gbdt)
    result.iloc[3,0]=metrics.roc_auc_score(y_test, pre_gbdt) 
    result.iloc[3,1]=metrics.accuracy_score(y_test, pre_gbdt)
    result.iloc[3,2]=metrics.precision_score(y_test, pre_gbdt)
    result.iloc[3,3]=metrics.recall_score(y_test, pre_gbdt)
    end=time.time()
    result.iloc[3,4]=end-start
    
    start=time.time()
    xg_reg=xgb.XGBClassifier(objective='binary:logistic'
                            ,learning_rat=0.1
                            ,max_depth=5
                            ,n_estimators=50
                            ,gamma=0.1
                            ,scale_pos_weight=1
                            ,min_child_weight=20
                            )
    xg_reg.fit(x_train,y_train)
    pred_xgb=xg_reg.predict(x_test)
    cm = confusion_matrix(y_test,pred_xgb)
    result.iloc[4,0]=metrics.roc_auc_score(y_test, pred_xgb) 
    result.iloc[4,1]=metrics.accuracy_score(y_test, pred_xgb)
    result.iloc[4,2]=metrics.precision_score(y_test, pred_xgb)
    result.iloc[4,3]=metrics.recall_score(y_test, pred_xgb)
    end=time.time()
    result.iloc[4,4]=end-start
#    print result.loc['xgb',:]
    
    '''
    xgb.plot_importance(xg_reg)
    
    data_dmatrix=xgb.DMatrix(data=x,label=y)
    params={'objective':'reg:linear','colsample_bytree':0.3
        ,'learning_rat':0.1,'max_depth':5,'alpha':10
        ,'min_child_weight':10}
 
    cv_result=xgb.cv(dtrain=data_dmatrix
                 ,params=params
                 ,nfold=5
                 ,num_boost_round=50
                 ,early_stopping_rounds=10
                 ,metrics='rmse'
                 ,as_pandas=True
                 ,seed=100)
    print result
'''
'''
xg_reg=xgb.XGBRegressor()
xg_reg.fit(x_train,y_train)
pred_xgb=xg_reg.predict(x_test)
aa=[]
for i in pred_xgb:
    if i>0.45:
        aa.append(1)
    else:
        aa.append(0)

cm = confusion_matrix(y_test,aa)
'''
'''
timeStamp = 1381419600
timeArray = time.localtime(timeStamp)
aa=time.strftime('%Y%m%d',timeArray)
'''
