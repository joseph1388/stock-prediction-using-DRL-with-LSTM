# -*- coding: utf-8 -*- 
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发


网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
  
文件名:ztools_sta.py
默认缩写：import ztools_sta as zsta
简介：Top极宽量化·回溯策略模块
 

'''
#

import sys,os,re
import arrow,bs4,random
import numexpr as ne  
import numpy as np
import pandas as pd
import tushare as ts
#import talib as ta

import pypinyin 
#

import matplotlib as mpl
from matplotlib import pyplot as plt

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
#import multiprocessing
#
import sklearn
from sklearn import metrics
#
import tflearn
import tensorflow as tf

#
import zsys
import zpd_talib as zta
import ztools as zt
import ztools_tq as ztq
import ztools_str as zstr
import ztools_data as zdat




#-------------------

#-------------sta.tools
def sta_buy(qx):
    stknum=0
    dprice=ztq.tq_stkGetPrice(qx.wrkStkDat,'dprice',qx.wrkTimStr)
    if dprice>0:
        if qx.trd_mode==1:stknum=qx.trd_buyNum;
        if qx.trd_mode==2:stknum=round(qx.trd_buyMoney/dprice)
        dcash,dsum=qx.usrMoney,stknum*dprice
        #
        if (dcash-dsum)<-qx.usrMoney0nil:stknum=0
        elif (dsum>dcash)and(not qx.trd_nilFlag):
            if qx.trd_mode==1:stknum=0
            if qx.trd_mode==2:stknum=dcash//dprice

    #
    return stknum


def sta_sell(qx):
    stknum,xcod=0,qx.wrkStkCod
    usr_stkNum=ztq.tq_usrPoolsGet(qx.usrPools,xcod,'num9')
    dprice=ztq.tq_stkGetPrice(qx.wrkStkDat,'dprice',qx.wrkTimStr)
    
    
    #
    if usr_stkNum>0:
        stknum=round(usr_stkNum*qx.trd_sellSize)
    elif qx.trd_nilFlag:
        if qx.trd_mode==1:stknum=qx.trd_buyNum;
        if qx.trd_mode==2:stknum=round(qx.trd_buyMoney/dprice)
    #
    #print('@sta-sell,',dprice,usr_stkNum,stknum,xcod)
    stknum=-stknum
    return stknum    
        
#-------------------sta
#----std.sta    
#----sta.avg01
    
def avg01_dpre(qx):
    xcod,ksgn,df=qx.wrkStkCod,qx.priceSgn,qx.wrkStkDat
    vn=qx.preVars[0]
    #
    df['dprice_max']=df[ksgn].rolling(vn).max()
    df['dprice_min']=df[ksgn].rolling(vn).min()
    df['dprice_avg']=df[ksgn].rolling(vn).mean()
    #
    qx.wrkStkDat=df
    return qx
    
    
def avg01(qx):
    stknum,xcod,df=0,qx.wrkStkCod,qx.wrkStkDat
    xtim,ksgn=qx.wrkTimStr,qx.priceSgn
    #
    dprice=ztq.tq_stkGetPrice(df,ksgn,xtim)
    dp_max=ztq.tq_stkGetPrice(df,'dprice_max',xtim)
    dp_min=ztq.tq_stkGetPrice(df,'dprice_min',xtim)
    dp_avg=ztq.tq_stkGetPrice(df,'dprice_avg',xtim)
    
    #
    kbuy,ksell=qx.staVars[0],qx.staVars[1]
    #fgBuy=(dprice<=(dp_min*kbuy))
    #fgSell=(dprice>=(dp_max*ksell))
    fgBuy=(dprice<=(dp_avg*kbuy))
    fgSell=(dprice>=(dp_avg*ksell))
    #
    if fgSell:stknum=sta_sell(qx)
    if fgBuy and(stknum==0):stknum=sta_buy(qx)
    #
    return stknum
    
#----ai.sta
#----sta.lstm01
    
def lstm010_dpre(qx):
    
    vn=qx.preVars[0]
    df,ksgn=qx.wrkStkDat,qx.priceSgn
    df=zdat.df_xed_nextDay(df,ksgn,'x'+ksgn,vn)   
    df['price_next']=df[zsys.xavg9Lst].max(axis=1)
    df['price'],df['y']=df[ksgn],df['price_next']
    #
    df['dprice_max']=df[ksgn].rolling(vn).max()
    df['dprice_min']=df[ksgn].rolling(vn).min()
    df['dprice_avg']=df[ksgn].rolling(vn).mean()
    #
    qx.wrkStkDat=df
    return qx
    
    
def lstm010(qx):
    stknum,xcod,df=0,qx.wrkStkCod,qx.wrkStkDat
    xtim,ksgn=qx.wrkTimStr,qx.priceSgn
    dprice=ztq.tq_stkGetPrice(df,'price',xtim)
    dp_max=ztq.tq_stkGetPrice(df,'dprice_max',xtim)
    dp_min=ztq.tq_stkGetPrice(df,'dprice_min',xtim)
    dp_avg=ztq.tq_stkGetPrice(df,'dprice_avg',xtim)
    #
    #dprice=ztq.tq_stkGetPrice(df,ksgn,xtim)
    d01=df[xtim:xtim]
    xdat=d01[zsys.TDS_xlst9].values
    xdat=xdat.astype(float)
    rxn,num_in=xdat.shape[0],len(zsys.TDS_xlst9)
    xdat=xdat.reshape(rxn,num_in,-1)
    #
    mx=qx.aiModel['lstm010']
    dp_y0 = mx.predict(xdat)   #y_pred
    y2=dp_y0.flatten()[:]
    dp_y=y2[0]
    #
    if dp_y>0:
        qx.wrkStkDat.ix[xtim,'price_next']=dprice
        #
        kbuy,ksell=qx.staVars[0],qx.staVars[1]
        #
        fgBuy=(dp_avg<=(dp_y*kbuy))
        fgSell=(dp_avg>=(dp_y*ksell))
        #
        #fgBuy=(dp_min>=(dp_y*kbuy))
        #fgSell=(dp_max<=(dp_y*ksell))
        #
        #fgBuy=(dprice>=(dp_y*kbuy))
        #fgSell=(dprice<=(dp_y*ksell))
        
        #
        if fgSell:stknum=sta_sell(qx)
        if fgBuy and(stknum==0):stknum=sta_buy(qx)  
        
    #
    return stknum
    
    #


#
#-------------------
'''
tn0=arrow.now()
y_pred = mx.predict(x_test)
tn=zt.timNSec('',tn0,True)
df_test['y_pred']=zdat.ds4x(y_pred,df_test.index,True)
df_test.to_csv('tmp/df_lstm010.csv',index=False)


#6
print('\n#6 acc准确度分析')
print('\nky0=10')
df=df_test
dacc,dfx,a10=ztq.ai_acc_xed2ext(df.y,df.y_pred,ky0=10,fgDebug=True)

'''

