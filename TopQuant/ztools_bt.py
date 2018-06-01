# -*- coding: utf-8 -*- 
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发


网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
  
文件名:ztools_bt.py
默认缩写：import ztools_bt as zbt
简介：Top极宽量化·回溯分析模块
 

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
#
import ztools as zt
import ztools_tq as ztq
import ztools_str as zstr
import ztools_sta as zsta
import ztools_data as zdat

 
#-------------------
#   bt.init
#qx.priceSgn,qx.priceDateFlag=priceSgn,priceDFlag
def bt_init_tim(qx,tim0Str,tim9Str=''):
    qx.wrkTimFmt=zt.iff2(qx.priceDateFlag,'YYYY-MM-DD','YYYY-MM-DD HH:mm:ss')
    if tim9Str=='':tim9Str=arrow.now().format(qx.wrkTimFmt)
    qx.btTim9=arrow.get(tim9Str)
    if tim0Str=='':
        qx.btTim0=qx.btTim9.shift(days=-29)
        tim0Str=qx.btTim0.format(qx.wrkTimFmt)
    else:    
        qx.btTim0=arrow.get(tim0Str)
    #    
    qx.btTim0Str,qx.btTim9Str=tim0Str,tim9Str
    qx.btTimNum=zt.timNDay(qx.btTim9,qx.btTim0)+1
    #print('\nqx.btTimNum-bt.init',qx.btTimNum)
    #
    #  btTimLst
    qx.btTimLst=[]
    for xcod in qx.inxCodeLst:
        df=qx.inxPools[xcod]
        mlst=list(df.index)
        qx.btTimLst=list(set(qx.btTimLst+mlst))
    #
    for xcod in qx.stkCodeLst:
        df=qx.stkPools[xcod]
        mlst=list(df.index)
        qx.btTimLst=list(set(qx.btTimLst+mlst))
    #
    
    qx.btTimLst=list(map(lambda x:zt.iff2(x>=qx.btTim0Str,x,''),qx.btTimLst))
    qx.btTimLst=list(map(lambda x:zt.iff2(x<=qx.btTim9Str,x,''),qx.btTimLst))
    qx.btTimLst=list(set(qx.btTimLst))
    qx.btTimLst.remove('')
    qx.btTimLst.sort(reverse=True)
    qx.btTimNum=len(qx.btTimLst)
    #
    xtim0,xtim9=qx.btTimLst[0],qx.btTimLst[-1]
    qx.btTim0Str,qx.btTim9Str=min(xtim0,xtim9),max(xtim0,xtim9)
    
    #
    return qx
    
#def sta_dataPre00(qx):
def bt_init_data(qx):    
    ksgn,df=qx.priceSgn,qx.wrkStkDat
    df=df.sort_index(ascending=True);
    #
    if ksgn=='avg':
        df[ksgn]=df[zsys.ohlcLst].mean(axis=1)
    else:
        df[ksgn]=df[ksgn]
    
    #
    df['dprice']=df[ksgn]
    df['dpricek']=df[ksgn].shift(-1)  #trd-price.next,day
    #
    df['xtim']=df.index
    df=zdat.df_xtim2mtim(df,'xtim',qx.priceDateFlag)
    #
    df=zta.mul_talib(zta.MA,df,ksgn,zsys.ma100Lst_var)
    #
    #df=df.round(2)
    #df=df.dropna()
    #qx.stkPools[xcod]=df.round(2)
    qx.wrkStkDat=df.round(3)
    
    #
    return qx
    
def bt_init(rdat,codLst,inxLst,tim0Str,tim9Str='',priceSgn='avg',prjNam='TQ01'):
    '''
    [输入参数]
        rdat，数据目录，一般日线数据是 rdatCN='/zDat/cn/day/'
        codLst,股票池代码列表
        inxLst,指数池代码列表
        vlst，bt回溯初始化变量参数列表
            [btTim0Str='',btTim9Str='']
    '''
    
    #
    #---set.bt.var
    #   set time
    
    #qx.btTim0Str,qx.btTim9Str=vlst[0],vlst[1]
    
    qx=ztq.tq_init(rdat,codLst,inxLst,priceSgn,prjNam)
    #tq_init(rs0,codLst,inxLst=['000001'],priceSgn='avg',priceDFlag=True,prjNam='TQ001'):
    #
    
    #
    ztq.tq_pools_call(qx,bt_init_data)
    qx=bt_init_tim(qx,tim0Str,tim9Str)
    
    #
    #b2=ztq.tq_trdObjInit(qx,0)
    #qx.trdLib=qx.trdLib.append(b2.T,ignore_index=True)
    qx.trdLib=pd.DataFrame(columns=zsys.qx_trdName,index=['ID']);   #所有交易记录清单列表         
    qx.trdLib.dropna(inplace=True);
    #
    qx.usrPools={}; #用户持有的股票资产数据 字典格式
    #
    qx.usrMoney0,qx.usrMoney,qx.usrTotal=zsys.qx_bt_money0,zsys.qx_bt_money0,zsys.qx_bt_money0
    qx.usrLevel=5
    qx.usrMoney0nil=qx.usrMoney0*qx.usrLevel
    #
    #qx.trd_mode,qx.trd_nilFlag=1,False
    ztq.tq_usrPoolsInit(qx,addFg=False)
    #
    xtim,qx.trdCnt=qx.btTim0Str,0
    qx.trdLib=pd.DataFrame(columns=zsys.qx_trdName,index=['ID']);   #所有交易记录清单列表         
    qx.trdLib.dropna(inplace=True);
    '''
    r1=pd.Series(zsys.qx_trdNil,index=zsys.qx_trdName);
    r1['cash'],r1['time']=qx.usrMoney0,qx.btTim0Str
    r1['ID']=ztq.tq_usrIDSet(qx)
    qx.trdLib=qx.trdLib.append(r1.T,ignore_index=True)
    ''' 
    #ztq.tq_usr2trdLib010(qx,xtim,'cash',0,0,0,qx.usrMoney0)
    #
    return qx
           
            
#-------------bt.work


def bt_main_1code(qx):
    #
    xcod,xtim=qx.wrkStkCod,qx.wrkTimStr
    dprice=ztq.tq_stkGetPrice(qx.wrkStkDat,qx.priceSgn,xtim)
    #
    qx.wrkStkNum=0
    if dprice>0:qx.wrkStkNum=qx.staFun(qx)
    #
    if qx.wrkStkNum!=0:
        usr_stkNum=ztq.tq_usrPoolsGet(qx.usrPools,xcod,'num9')
        #  
        dnum,dcash=qx.wrkStkNum,qx.usrMoney
        qx.usrMoney=dcash-dnum*dprice
        num9=usr_stkNum+dnum
        #
        ztq.tq_usrPoolsPutAll(qx.usrPools,xcod,num9,dnum)
    #
    return qx

def bt_main_1day_pools(qx):
    ztq.tq_usrPoolsInit(qx,addFg=True)
    trdFg=False
    for xcod in qx.stkCodeLst:
        qx.wrkStkCod=xcod
        qx.wrkStkDat=qx.stkPools[xcod]
        #
        bt_main_1code(qx)
        if qx.wrkStkNum!=0:trdFg=True
    #
    if trdFg:ztq.tq_usr2trdLib(qx)
        
    #
    return qx
    


def bt_main(qx):
    #bt 8 code
    #
    #ztq.tq_pools_call(qx,bt_init_dadattmain_1day1code)
    #
    qx.btTimLst.sort(reverse=False)
    for tc,xtim in enumerate(qx.btTimLst):
    #for xtim in range(qx.btTimLst):
        #xtim=qx.btTimLst[tc]
        print(tc,xtim)
        
        #
        qx.wrkTimStr,qx.wrkTim=xtim,arrow.get(xtim)
        #
        qx=bt_main_1day_pools(qx)
        #
        #ztq.tq_prTrdlib(qx)
        #ztq.tq_prUsrPools(qx.usrPools,'qx.usrPools')
    #
    ztq.tq_usrPoolsInit(qx,addFg=True)
    return qx
    
