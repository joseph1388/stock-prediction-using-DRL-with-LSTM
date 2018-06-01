# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 
网站:www.TopQuant.vip   www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
     
TopQuant-极宽量化程序
@ www.TopQuant.vip      www.ziwang.com
 by Top极宽·量化开源团队 2016.12.25 首发

  
文件名:zai_sklearn.py
默认缩写：import zai_sklearn as zsk
简介：Top极宽量化·sklearnAI智能分析模块
 
'''
#

import sys,os,re
import os,sys,re
import arrow,random

import numpy as np
import pandas as pd
import tushare as ts
import numexpr as ne  


import matplotlib as mpl
from matplotlib import pyplot as plt

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

#
import sklearn 
from sklearn import datasets, linear_model
from sklearn import metrics
from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import BernoulliRBM
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib 
#
#
#
import zsys
import ztools as zt
import zpd_talib as zta
import zai_tools as zat
#


'''
#----------ai.const&var.xxx
#----------ai.misc.xxx
#----------ai.data.xxx
#----------ai.mx.xxx
#--------mx.fun.sgn
#--------mx.fun.xxx

#--------mx.call.xxx
#
#--------ai.f(ile).xxx    
'''

        
#----------ai.xxx
#----------ai.const&var.xxx

        
#----------fb.model.x.xxx
#线性回归算法，最小二乘法，函数名，LinearRegression
def mx_line(train_x, train_y):
    mx = LinearRegression()
    mx.fit(train_x, train_y)
    #print('\nlinreg.intercept_')
    #print (mx.intercept_);print (mx.coef_)
    #linreg::model
    #
    return mx
    
# 逻辑回归算法，函数名，LogisticRegression
def mx_log(train_x, train_y):
    
    mx = LogisticRegression(penalty='l2')
    mx.fit(train_x, train_y)
    return mx
    
    
# 多项式朴素贝叶斯算法，Multinomial Naive Bayes，函数名，multinomialnb
def mx_bayes(train_x, train_y):
    
    mx = MultinomialNB(alpha=0.01)
    mx.fit(train_x, train_y)
    return mx


# KNN近邻算法，函数名，KNeighborsClassifier
def mx_knn(train_x, train_y):
    
    mx = KNeighborsClassifier()
    mx.fit(train_x, train_y)
    return mx




# 随机森林算法， Random Forest Classifier, 函数名，RandomForestClassifier
def mx_forest(train_x, train_y):
    
    mx = RandomForestClassifier(n_estimators=8)
    mx.fit(train_x, train_y)
    return mx


# 决策树算法，函数名，tree.DecisionTreeClassifier()
def mx_dtree(train_x, train_y):
    
    mx = tree.DecisionTreeClassifier()
    mx.fit(train_x, train_y)
    return mx


# GBDT迭代决策树算法，Gradient Boosting Decision Tree，
# 又叫 MART(Multiple Additive Regression Tree)，函数名，GradientBoostingClassifier
def mx_GBDT(train_x, train_y):
    
    mx = GradientBoostingClassifier(n_estimators=200)
    mx.fit(train_x, train_y)
    return mx


# SVM向量机算法，函数名，SVC
def mx_svm(train_x, train_y):
    
    mx = SVC(kernel='rbf', probability=True)
    mx.fit(train_x, train_y)
    return mx

# SVM- cross向量机交叉算法，函数名，SVC
def mx_svm_cross(train_x, train_y):
    
    mx = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(mx, param_grid, n_jobs = 1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    #for para, val in best_parameters.items():
    #    print( para, val)
    mx = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    mx.fit(train_x, train_y)
    return mx
    

#----神经网络算法

    
# MLP神经网络算法    
def mx_MLP(train_x, train_y):    
    #mx = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1) 
    mx = MLPClassifier() 
    mx.fit(train_x, train_y)
    return mx

# MLP神经网络回归算法
def mx_MLP_reg(train_x, train_y):    
    #mx = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1) 
    mx = MLPRegressor() 
    mx.fit(train_x, train_y)
    return mx
    
    
#--------mx.fun.sgn
mxfunLst=['line','log','bayes','knn','forest','dtree','gbdt','svm','svmcr','mlp','mlpreg']
mxfunSgn={'line':mx_line,
          'log':mx_log,
          'bayes':mx_bayes,
          'knn':mx_knn,
          'forest':mx_forest,
          'dtree':mx_dtree,
          'gbdt':mx_GBDT,
          'svm':mx_svm,
          'svmcr':mx_svm_cross,
          'mlp':mx_MLP,
          'mlpreg':mx_MLP_reg
          }
xmodel={}
'''
xmodel={'line':'','log':'','bayes':'','knn':''
          'forest':mx_forest,
          'dtree':mx_dtree,
          'gbdt':mx_GBDT,
          'svm':mx_svm,
          'svmcr':mx_svm_cross,
          'mlp':mx_MLP,
          'mlpreg':mx_MLP_reg
          }
'''
#--------mx.fun.xxx
#极宽机器学习接口函数
def mx_fun010(funSgn,x_train, x_test, y_train, y_test,yk0=5,fgInt=False,fgDebug=False):
    #1
    df9=x_test.copy()
    mx_fun=mxfunSgn[funSgn]
    mx =mx_fun(x_train.values,y_train.values)
    #2
    y_pred = mx.predict(x_test.values)
    df9['y_test'],df9['y_pred']=y_test,y_pred
    #3   
    if fgInt:
        df9['y_predsr']=df9['y_pred']
        df9['y_pred']=round(df9['y_predsr']).astype(int)
        
    #4
    dacc=zat.ai_acc_xed(df9,yk0,fgDebug)
    #5
    if fgDebug:
        #print(df9.head())
        print('@fun name:',mx_fun.__name__)
        df9.to_csv('tmp/df9_pred.csv');
    #
    #6
    print('@mx:mx_sum,kok:{0:.2f}%'.format(dacc))   
    return dacc,df9   

#极宽机器学习批量调用函数    
def mx_funlst(funlst,x_train, x_test, y_train, y_test,yk0=5,fgInt=False):
    for funsgn in funlst:
        print('\n',funsgn)
        tim0=arrow.now()
        mx_fun010(funsgn,x_train, x_test, y_train, y_test,yk0,fgInt)
        zt.timNSec('',tim0,True)
        
#极宽调用算法模型接口函数        
def mx_fun8mx(mx,x_test,y_test,yk0=5,fgInt=False,fgDebug=False):
    #1
    df9=x_test.copy()
    #mx=....
    #2
    y_pred = mx.predict(x_test.values)
    df9['y_test'],df9['y_pred']=y_test,y_pred
    #3   
    if fgInt:
        df9['y_predsr']=df9['y_pred']
        df9['y_pred']=round(df9['y_predsr']).astype(int)
        
    #4
    dacc=zat.ai_acc_xed(df9,yk0,fgDebug)
    #5
    if fgDebug:
        #print(df9.head())
        #print('@fun name:',mx_fun.__name__)
        df9.to_csv('tmp/df9_pred.csv',index=False);
    #
    #6
    #print('@mx:mx_sum,kok:{0:.2f}%'.format(dacc))   
    return dacc,df9       

#极宽批量调用算法模型接口函数        
def mx_funlst8mx(mxlst, x_test,  y_test,yk0=5,fgInt=False):
    for msgn in mxlst:
        #print('@msgn:',msgn)
        tim0=arrow.now()
        mx=xmodel[msgn]
        dacc,df9=mx_fun8mx(mx, x_test, y_test,yk0,fgInt)
        tn=zt.timNSec('',tim0)
        xss='ok:{0:.2f}%,mx,{1},tn,{2:.2f} s'.format(dacc,msgn,tn)
        print(xss)   
        

#----mx.mul.xxx    

    
#极宽机器学习组合算法函数
def mx_mul(mlst, x_test,  y_test,yk0=5,fgInt=False,fgDebug=False):    
    #1
    print('\ny_pred,预测')
    df9,xc,mxn9=x_test.copy(),0,len(mlst)
    df9['y_test']=y_test
    #2   
    for msgn in mlst:
        xc+=1;tim0=arrow.now()
        mx=xmodel[msgn]
        y_pred = mx.predict(x_test.values)
        #3
        if xc==1:df9['y_sum']=y_pred
        else:df9['y_sum']=df9['y_sum']+y_pred            
        #4
        tn=zt.timNSec('',tim0)
        df9['y_pred']=y_pred
        #4.b   
        if fgInt:
            df9['y_predsr']=df9['y_pred']
            df9['y_pred']=round(df9['y_predsr']).astype(int)
       
        #5   
        dacc=ai_acc_xed(df9,yk0,fgDebug)
        xss='y_pred{0:02},kok:{1:.2f}%'.format(xc,dacc);print(xc,xss,msgn,tn,'s')
        ysgn='y_pred'+str(xc);df9[ysgn]=y_pred
    #6
    df9['y_pred']=df9['y_sum']/mxn9
    
    if fgInt:
        df9['y_predsr']=df9['y_pred']
        df9['y_pred']=round(df9['y_predsr']).astype(int)
        
    #7    
    dacc=zat.ai_acc_xed(df9,yk0,fgDebug)    
    #8
    if fgDebug:
        df9.to_csv('tmp/df9_pred.csv');
   
    #9
    print('@mx:mx_sum,kok:{0:.2f}%'.format(dacc))   
    return dacc,df9        

             
#-----mx_fun_call        


#极宽一体化机器学习调用函数    
def mx_fun_call(df,xlst,ysgn,funSgn,yksiz=1,yk0=5,fgInt=False,fgDebug=False):
    #1
    df[ysgn]=df[ysgn].astype(float)
    df[ysgn]=round(df[ysgn]*yksiz).astype(int)
    
    
    #2
    x,y= df[xlst],df[ysgn]  
    #3
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
    num_train, num_feat = x_train.shape
    num_test, num_feat = x_test.shape
    print('\nn_tran:,',num_train,' ,ntst,' , num_test, ' ,dimension:,',num_feat,',kbin,',fgInt)
    
    #4
    print('\ny_pred,预测')
    df9=x_test.copy()
    mx_fun=mxfunSgn[funSgn]
    mx =mx_fun(x_train.values,y_train.values)
    #5
    y_pred = mx.predict(x_test.values)
    df9['y_test'],df9['y_pred']=y_test,y_pred
    #6
    if fgInt:
        df9['y_predsr']=df9['y_pred']
        df9['y_pred']=round(df9['y_predsr']).astype(int)
        
    #7
    dacc=zat.ai_acc_xed(df9,yk0,fgDebug)
    #8
    if fgDebug:
        #print(df9.head())
        print('@fun name:',mx_fun.__name__)
        df.to_csv('tmp/df_sr.csv');
        df9.to_csv('tmp/df9_pred.csv');
    #------------
    #9
    print('@mx:mx_sum,kok:{0:.2f}%'.format(dacc))   
    return dacc,df9    
        

     
    
#------------
#--------ai.f.xxx    
#保存算法模型文件
def ai_f_mxWr(ftg,funSgn,x_train, y_train):
    #1
    mx_fun=mxfunSgn[funSgn]
    mx =mx_fun(x_train.values,y_train.values)    
    #2
    joblib.dump(mx,ftg) 
    
#批量保存算法模型文件    
def ai_f_mxWrlst(ftg0,funlst,x_train, y_train):
    for funSgn in funlst:
        ftg=ftg0+funSgn+'.pkl'
        print('\n',ftg)
        tim0=arrow.now()
        ai_f_mxWr(ftg,funSgn,x_train, y_train)
        zt.timNSec('',tim0,True)    

#批量读取算法模型文件
def ai_f_mxRdlst(fsr0,funlst):
    for funSgn in funlst:
        fss=fsr0+funSgn+'.pkl'
        print(fss)
        xmodel[funSgn]=joblib.load(fss)
        
        
        
#----ai.f.dat.xxx    
#单组数据读取函数    
def ai_f_datRd010(fsr,k0=0,fgPr=False):
    #1
    df=pd.read_csv(fsr,index_col=False);
    #2
    if k0>0:
        ysgn=df.columns[0];#print('y',ysgn)
        df[ysgn]=round(df[ysgn]*k0).astype(int)
        
    #3
    if fgPr:
        print('\n',fsr);print(df.tail())
        
    #4
    return  df
        
#双组数据读取函数
def ai_f_datRd020(fsr,xlst,ysgn,k0=1,fgPr=False):    
    
    #1
    df=pd.read_csv(fsr,index_col=False,encoding='gb18030')
    #2
    df[ysgn]=df[ysgn].astype(float)
    df[ysgn]=round(df[ysgn]*k0).astype(int)              
    #3              
    x_dat,y_dat= df[xlst],df[ysgn]   
      
    #4
    if fgPr:
        print('\n',fsr);
        print('\nx_dat');print(x_dat.tail())
        print('\ny_dat');print(y_dat.tail())
        
        
    #5
    return  x_dat,y_dat
        
#多组数据读取函数
def ai_f_datRd(fsr0,k0=1,fgPr=False):    
    #1
    fss=fsr0+'xtrain.csv';x_train=pd.read_csv(fss,index_col=False);print(fss)
    fss=fsr0+'xtest.csv';x_test=pd.read_csv(fss,index_col=False);print(fss)
    fss=fsr0+'ytrain.csv';y_train=pd.read_csv(fss,index_col=False);print(fss)
    fss=fsr0+'ytest.csv';y_test=pd.read_csv(fss,index_col=False);print(fss)
    #2
    ysgn=y_train.columns[0];#print('y',ysgn)
    y_train[ysgn]=round(y_train[ysgn]*k0).astype(int)
    y_test[ysgn]=round(y_test[ysgn]*k0).astype(int)
    #3
    if fgPr:
        print('\nx_train');print(x_train.tail())
        print('\nx_test');print(x_test.tail())
        print('\ny_train');print(y_train.tail())
        print('\ny_test');print(y_test.tail())        
    #4
    return  x_train, x_test, y_train, y_test    

#===========
'''


'''       