# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 
网站:www.TopQuant.vip   www.ziwang.com
QQ总群:124134140   千人大群 zwPython量化&大数据 
   
TopQuant-极宽量化程序
@ www.TopQuant.vip      www.ziwang.com
 by Top极宽·量化开源团队 2016.12.25 首发

  
文件名:zai_tools.py
默认缩写：import zai_tools as zat
简介：Top极宽量化·常用AI工具辅助函数

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
 
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

#----------ai.misc.xxx

#结果验证函数
def ai_acc_xed(df9,ky0=5,fgDebug=True):
    #1
    #ny_test,ny_pred=len(df9['y_test']),len(df9['y_pred'])
    ny_test=len(df9['y_test'])
    df9['ysub']=df9['y_test']-df9['y_pred']
    df9['ysub2']=np.abs(df9['ysub'])
    #2
    df9['y_test_div']=df9['y_test']
    df9.loc[df9['y_test'] == 0, 'y_test_div'] =0.00001
    df9['ysubk']=(df9['ysub2']/df9['y_test_div'])*100
    dfk=df9[df9['ysubk']<ky0]   
    dsum=len(dfk['y_pred'])
    dacc=dsum/ny_test*100
    #
    #3
    if fgDebug:
        print('\nai_acc_xed')
        print(df9.head())
        y_test,y_pred=df9['y_test'],df9['y_pred']
        print('\nn_df9,{0},n_dfk,{1}'.format(ny_test,dsum))
        dmae=metrics.mean_absolute_error(y_test, y_pred)
        dmse=metrics.mean_squared_error(y_test, y_pred)
        drmse=np.sqrt(metrics.mean_squared_error(y_test, y_pred))
        print('acc-kok: {0:.2f}%, MAE:{1:.2f}, MSE:{2:.2f}, RMSE:{3:.2f}'.format(dacc,dmae,dmse,drmse))
        
    #
    #4
    return dacc    
    
#----------ai.data.xxx    
#数据切割函数    
def ai_data_cut(df,xlst,ysgn,ftg0,fgPr=False):
    x,y= df[xlst],df[ysgn]      
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
    #
    fss=ftg0+'xtrain.csv';x_train.to_csv(fss,index=False);print(fss)
    fss=ftg0+'xtest.csv';x_test.to_csv(fss,index=False);print(fss)
    fss=ftg0+'ytrain.csv';y_train.to_csv(fss,index=False,header=True);print(fss)
    fss=ftg0+'ytest.csv';y_test.to_csv(fss,index=False,header=True);print(fss)
    #
    if fgPr:
        print('\nx_train');print(x_train.tail())
        print('\nx_test');print(x_test.tail())
        print('\ny_train');print(y_train.tail())
        print('\ny_test');print(y_test.tail())       
   
#数据读取函数，新版本名称为ai_f_datRd     
def ai_dat_rd(fsr0,k0=1,fgPr=False):    
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

        

 