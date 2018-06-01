#coding=utf-8
# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 


网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
    
TopQuant.vip ToolBox 2016
Top极宽·量化开源工具箱 系列软件 
by Top极宽·量化开源团队 2016.12.25 首发
  
文件名:ztools_data.py
默认缩写：import ztools_datadown as zddown
简介：Top极宽常用数据现在工具函数集
'''

import os,sys,io,re
import random,arrow,bs4
import numpy as np
import numexpr as ne
import pandas as pd
import tushare as ts

import requests
#
import cpuinfo as cpu
import psutil as psu
import inspect
#
import matplotlib as mpl
import matplotlib.colors
from matplotlib import cm

#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_web as zweb
import ztools_data as zdat

#

#-----------------------

#-----------------------
#-------down_stk.xxx

#-------down_stk.base
def down_stk_base():        
    '''
    下载时基本参数数据时，有时会出现错误提升：
          timeout: timed out
          属于正常现象，是因为网络问题，等几分钟，再次运行几次 
          '''
    rss="tmp\\"
    #
    fss=rss+'stk_inx0.csv';print(fss);
    dat = ts.get_index()
    dat.to_csv(fss,index=False,encoding='gbk',date_format='str');

    #=========
    fss=rss+'stk_base.csv';print(fss);
    dat = ts.get_stock_basics();
    dat.to_csv(fss,encoding='gbk',date_format='str');
    
    c20=['code','name','industry','area'];
    d20=dat.loc[:,c20]
    d20['code']=d20.index;
    
    fss=rss+'stk_code.csv';print(fss);
    d20.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
    #sz50,上证50；hs300,沪深300；zz500，中证500
    fss=rss+'stk_sz50.csv';print(fss);
    dat=ts.get_sz50s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
    fss=rss+'stk_hs300.csv';print(fss);
    dat=ts.get_hs300s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');

    fss=rss+'stk_zz500.csv';print(fss);
    dat=ts.get_zz500s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
        
#-------down_stk.inx.xxx    
        

def down_stk_inx010(rdat,xcod,tim0):
    ''' 下载大盘指数数据,简版股票数据，可下载到1994年股市开市起
    【输入】
        xcod:指数代码
        rdat,数据文件目录
        tim0,数据起始时间
        

    '''
    xd=[];fss=rdat+xcod+'.csv';
    if tim0=='':tim0='1994-01-01';
    #print('f,',fss)
    #-------------------
    xfg=os.path.exists(fss);xd0=[];
    if xfg:xd0,tim0=zdat.df_rdcsv_tim0(fss,'date',tim0)
    
    #    
    print('\n',xfg,fss,",",tim0);   
    #-----------    
    try:
        #xd=ts.get_h_data(xcod,start=tim0,index=True,end=None,retry_count=5,pause=1)     #Day9     
        xdk=ts.get_k_data(xcod, index=True,start=tim0,end=None)
        xd=xdk
        #-------------
        if len(xd)>0:
            if (len(xd0)>0):         
                xd=xdk[zsys.ohlcDVLst]
                xd=zdat.df_xappend(xd,xd0,'date')
            #print('\nxd5\n',xd.head())
            xd=xd.sort_values(['date'],ascending=False);
            xd.to_csv(fss,index=False,encoding='gbk')
    except IOError: 
        pass    #skip,error
    
           
    return xd    


    
def down_stk_inx(rdat,finx):
    dinx = pd.read_csv(finx,encoding='gbk');print(finx); 
    xn9=len(dinx['code']);
    for i in range(xn9):
    #for xc,xtim0 in dinx['code'],dinx['tim0']:
        d5=dinx.iloc[i]
        xc=d5['code'];xtim0=d5['tim0']
        i+=1;code="%06d" %xc
        print("\n",i,"/",xn9,"code,",code,xtim0)
        #---
        down_stk_inx010(rdat,code,xtim0)
        
#-------down_stk.day.xxx      
       

      

def down_stk010(rdat,xcod,xtyp,fgInx=False):
    ''' 中国A股数据下载子程序
    【输入】
        xcod:股票代码
        rdat,数据文件目录
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟

    '''
    
    tim0,fss='1994-01-01',rdat+xcod+'.csv'
    xfg=os.path.exists(fss);xd0=[];xd=[];
    if xfg:
        xd0,tim0=zdat.df_rdcsv_tim0(fss,'date',tim0)
        
    print('\t',xfg,fss,",",tim0)
    #-----------    
    try:
        xdk=ts.get_k_data(xcod, index=fgInx,start=tim0,end=None,ktype=xtyp);
        xd=xdk
        #-------------
        if len(xd)>0:
            xd=xdk[zsys.ohlcDVLst]
            xd=zdat.df_xappend(xd,xd0,'date')
            #
            xd=xd.sort_values(['date'],ascending=False);
            xd.to_csv(fss,index=False,encoding='gbk')
    except IOError: 
        pass    #skip,error
    
           
    return xd  

def down_stk_all(rdat,finx,xtyp='D',fgInx=False):
    '''
    根据finx股票列表文件，下载所有，或追加日线数据
    自动去重，排序
    
    '''
    stkPool = pd.read_csv(finx,encoding='gbk') ;print(finx);
    xn9=len(stkPool['code']);
    for i,xc in enumerate(stkPool['code']):
        code="%06d" %xc
        print("\n",i,"/",xn9,"code,",code)
        #---
        down_stk010(rdat,code,xtyp);
            
        
#------down__tick.xxx
        
def down_tick010(xcod,xtim,ftg):
    '''
    根据指定的日期，股票代码，数据文件名：ftg
    下载指定股票指定日期的ticks数据，并保存到ftg
    [输入]
        xcode，股票代码
        xtim，当前日期的字符串
        ftg，保存tick数据的文件名
    '''
    df,dn=[],0
    try:
        df = ts.get_tick_data(xcod,date=xtim)    #print(df.head())
    except IOError: 
        pass    #skip,error 
    datFlag,dn=False,len(df); # print('     n',dn,ftg) # 跳过无数据 日期
    #if zwt.xin(dn,0,9):print('n2',dn,ftg) 
    if dn>10:  
        df['type']=df['type'].str.replace(u'中性盘', 'norm');
        df['type']=df['type'].str.replace(u'买盘', 'buy');
        df['type']=df['type'].str.replace(u'卖盘', 'sell');
        df.to_csv(ftg,index=False,encoding='utf') 
        datFlag=True
    #
    return datFlag,dn,df        

def down_tickLib8tim(rs0,stkPool,xtim):
    '''
    下载指定日期，stkCodeLib包含的所有代码的tick历史分笔数据
    并转换成对应的分时数据：5/15/30/60 分钟
    数据文件保存在：对应的数据目录 \zwdat\tick\yyyy-mm\
        目录下，yyyy，是年份；mm，是月份
    运行时，会根据日期，股票代码，生成数据文件名：ftg
    [输入]
      rs0,保存tick数据的目录
      stkCodeLib，包含所有股票代码的pd数据表格
      xtim，当前日期，格式：yyyy-mm-dd
          '''
    #qx.xday0ChkFlag=False self.codeInx0k=-1
    #inx0,qx.codeNum=qx.codeInx,len(dinx['code']);
    s2=xtim.split('-')
    mss=s2[0]+'-'+s2[1]
    rss=rs0+mss+'/'
    xfg=os.path.exists(rss)
    if not xfg:os.mkdir(rss)
    #
    numNil,num_code=0,len(stkPool)
    for i,xc in enumerate(stkPool['code']):
        code="%06d" %xc;#print("\n",i,"/",qx.codeNum,"code,",code)
        #code,qx.codeCnt=code,i
        #--- 
        #ftg='%s%s_%s.csv'%(qx.rtickTimMon,code)
        ftg='%s%s_%s.csv'%(rss,code,xtim);
        xfg=os.path.exists(ftg);  
        if xfg:
            numNil=0
        else:
            if numNil<90:
                datFlag,dfNum,df=down_tick010(code,xtim,ftg)
                numNil=zt.iff2(datFlag,0,numNil+1)
                if dfNum==3:numNil+=10;
            #
            print(xfg,datFlag,i,"/",num_code,ftg,numNil)
        #
        if numNil>90:break
        #if i>3:break
    
def down_tickLib8tim_mul(rs0,stkPool,xtim0,xtim9):
    '''
    下载所有股票代码的所有tick历史分笔数据，按时间日期循环下载
    数据文件保存在：对应的数据目录 \zwdat\tick\yyyy-mm\
        目录下，yyyy，是年份；mm，是月份
    [输入]
      rs0,保存tick数据的目录
      stkCodeLib，包含所有股票代码的pd数据表格
      xtim0，起始日期，格式：yyyy-mm-dd
      xtim9，结束日期，格式：yyyy-mm-dd
      '''
    
    #xtick_down_init(qx,finx)
    #qx.xday0ChkFlag=False
    #print('r',qx.rdat,qx.rtickTim);
    #    self.rtickTimMon=self.rtickTim+'2010-01\\';  #   \zwDat\ticktim\  2012-01\
    nday=zt.timNDayStr(xtim9,xtim0)+1
    tim0=arrow.get(xtim0)
    print('t0,',tim0,nday)
    for tc in range(nday):
        #qx.DTxtim=qx.DTxtim0+dt.timedelta(days=tc) 
        #qx.xdayInx,qx.xtimSgn=tc,qx.DTxtim.strftime('%Y-%m-%d'); 
        #
        #
        xtim=tim0.shift(days=tc)
        xtimSgn=xtim.format('YYYY-MM-DD')
        #print(tc,'#,xtim,',xtimSgn)
        print('\n',tc,'/',nday,xtimSgn)
        #
        #xtick_down8tim_codes(qx)    
        down_tickLib8tim(rs0,stkPool,xtimSgn)
        
#------------donw_min.real__

def down_min_real010(rdat,xcod,xtyp='5',fgIndex=False):
    ''' 下载大盘指数数据,简版股票数据，可下载到1994年股市开市起
    【输入】
        rdat,数据文件目录
        xcod:股票、指数代码
        finx:股票、指数代码文件
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟    
        fgIndex,指数下载模式；默认为 False，股票下载模式。
    
        

    '''
    xd=[]
    xtim=arrow.now().format('YYYY-MM-DD')
    fss=rdat+xcod+'.csv';
    if fgIndex:fss=rdat+'inx_'+xcod+'.csv';
    #print('f,',fss)
    print('\n',fss,",",xtim);   
    #-----------    
    try:
        xd=ts.get_k_data(xcod, index=fgIndex,start=xtim,end=xtim,ktype=xtyp)
        #-------------
        if len(xd)>0:
            xd=xd[zsys.ohlcDVLst]
            #print('\nxd5\n',xd.head())
            xd=xd.sort_values(['date'],ascending=True);
            xd=xd[xd.date>xtim]
            xd.to_csv(fss,index=False,encoding='gbk')
    except IOError: 
        pass    #skip,error
    
           
    return xd    
                

def down_min_all(rdat,finx,xtyp='5',fgIndex=False):
    '''
    根据finx列表文件，下载所有股票、指数实时数据
    【输入】
        rdat,数据文件目录
        finx:股票、指数代码文件
        xtyp (str)：k线数据模式，默认为D，日线
            D=日 W=周 M=月 ；5=5分钟 15=15分钟 ，30=30分钟 60=60分钟    
        fgIndex,指数下载模式；默认为 False，股票下载模式。
    
    
    '''
    stkPool = pd.read_csv(finx,encoding='gbk') ;print(finx);
    xn9=len(stkPool['code']);
    for i,xc in enumerate(stkPool['code']):
        code="%06d" %xc
        print("\n",i,"/",xn9,"code,",code)
        #---
        down_min_real010(rdat,code,xtyp,fgIndex)
        