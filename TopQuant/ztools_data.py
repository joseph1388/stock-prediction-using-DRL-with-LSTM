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
默认缩写：import ztools_data as zdat
简介：Top极宽常用数据工具函数集
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
import zpd_talib as zta

#

#-----------------------
'''

misc
#
df.xxx,pandas.xxx
    df.cov.
    df.get.
    df.cut.
#

'''

#-----------------------
#----------data.misc


#-----Series

    
def ds4x(x,inx=None,fgFlat=False):
    if fgFlat:
        x=x.flatten()[:]
    #
    ds=pd.Series(x)
    if len(inx)>0: ds.index=inx
    #
    return ds


#----------df.misc
#df['ktype']=np.round(df['price_change'])

#df['ktype'][df.ktype<900]=900
#df['close'][df.close>1100]=1100

def df2type20(df,ksgn='ktype',n9=10):
    #dsk
    #df['price_change']=df['price_next']/df['price']*100
    #
    df[ksgn]=np.round(df[ksgn])
    d0,d9=100-n9,100+n9
    #if df[ksgn]:
    df[ksgn][df[ksgn]<d0]=d0
    df[ksgn][df[ksgn]>d9]=d9
    df['ktype']=df['ktype'].astype(int)
    #
    return df



def df_xshift(df,ksgn='avg',num9=10):
    xsgn='x'+ksgn
    alst=[xsgn]
    df[xsgn]=df[ksgn].shift(-1)
    for xc in range(2,num9):
       xss=xsgn+'_'+str(xc)   
       df[xss]=df[ksgn].shift(-xc)
       alst.append(xss)
    #
    return df,alst
    
#----------df2type
def df_type2float(df,xlst):
    for xsgn in xlst:
        df[xsgn]=df[xsgn].astype(float)

def df_type4mlst(df,nlst,flst):
    for xsgn in nlst:
        df[xsgn]=df[xsgn].astype(int)
        
    for xsgn in flst:
        df[xsgn]=df[xsgn].astype(float)
        
            
    
#----------df.xxx,pandas.xxx

#----------df.cov.xxx,pandas.xxx       
def df_2ds8xlst(df,ds,xlst):
    for xss in xlst:
        ds[xss]=df[xss]
    #
    
    #df9.to_csv(ftg,index=False,encoding='gbk')
    return ds
    
#----------df.get.xxx,pandas.xxx       
def df_get8tim(df,ksgn,kpre,kn9,kpos):
    #@ zdr.dr_df_get8tim
    #
    xdf=pd.DataFrame(columns=['nam','dnum'])
    ds=pd.Series(['',0],index=['nam','dnum'])
    for xc in range(1,kn9+1):
        xss,kss='{0:02d}'.format(xc),'{0}{1:02d}'.format(kpre,xc)
        df2=df[df[ksgn].str.find(kss)==kpos]
        ds['nam'],ds['dnum']=xss,len(df2['gid'])
        xdf=xdf.append(ds.T,ignore_index=True)
        #print(xc,'#',xss,kss)
    #
    xdf.index=xdf['nam']
    return xdf


 
#
    
    
#----------df.cut.xxx,pandas.xxx            
def df_kcut8tim(df,ksgn,tim0str,tim9str):
    if ksgn=='':
        df2=df[tim0str<=df.index]
        df3=df2[df2.index<=tim9str]
    else:
        df2=df[tim0str<=df[ksgn]]
        df3=df2[df2[ksgn]<=tim9str]
    #
    return df3
        
def df_kcut8yearlst(df,ksgn,ftg0,yearlst):
    for ystr in yearlst:
        tim0str,tim9str=ystr+'-01-01',ystr+'-12-31'
        df2=df_kcut8tim(df,ksgn,tim0str,tim9str)
        ftg=ftg0+ystr+'.dat';print(ftg)
        df2.to_csv(ftg,index=False,encoding='gb18030')
    
def df_kcut8myearlst(df,ksgn,tim0str,ftg0,yearlst):
    for ystr in yearlst:
        tim9str=ystr+'-12-31'
        df2=df_kcut8tim(df,ksgn,tim0str,tim9str)
        ftg=ftg0+ystr+'.dat';print(ftg)
        df2.to_csv(ftg,index=False,encoding='gb18030')
    
#----------df.xed
def df_xappend(df,df0,ksgn,num_round=3,vlst=zsys.ohlcDVLst):
    if (len(df0)>0):   
        df2 =df0.append(df)     
        df2=df2.sort_values([ksgn],ascending=True);
        df2.drop_duplicates(subset=ksgn, keep='last', inplace=True);
        #xd2.index=pd.to_datetime(xd2.index);xd=xd2
        df=df2
        
    #
    df=df.sort_values([ksgn],ascending=False);
    df=np.round(df,num_round);
    df2=df[vlst]
    #
    return df2
    
#----------df.xtim.xxx

def df_xtim2mtim(df,ksgn='xtim',fgDate=False):    
    df['xyear']=df[ksgn].apply(zstr.str_2xtim,ksgn='y')
    df['xmonth']=df[ksgn].apply(zstr.str_2xtim,ksgn='m')
    df['xday']=df[ksgn].apply(zstr.str_2xtim,ksgn='d')
    #
    df['xday_week']=df[ksgn].apply(zstr.str_2xtim,ksgn='dw')
    df['xday_year']=df[ksgn].apply(zstr.str_2xtim,ksgn='dy')
    #df['xday_month']=df['xtim'].apply(zstr.str_2xtim,ksgn='dm')
    df['xweek_year']=df['xtim'].apply(zstr.str_2xtim,ksgn='wy')
    #
    df['xhour']=df[ksgn].apply(zstr.str_2xtim,ksgn='h')
    df['xminute']=df[ksgn].apply(zstr.str_2xtim,ksgn='t')
    
    #
    if fgDate:
        df=df.drop(['xhour','xminute'],axis=1)
    #
    return df

#----------df.xdat.ed.xxx
def df_xed_nextDay(df,ksgn='avg',newSgn='xavg',nday=10):    
    #df['avg']=df[zsys.ohlcLst].mean(axis=1).round(2)
    for i in range(1,nday):
        xss=newSgn+str(i)
        df[xss]=df[ksgn].shift(-i)
    #
    return df
    
        
def df_xed_ailib(df,ksgn='avg',fgDate=True):
    #   xed.avg
    df=df.sort_index(ascending=True);
    if ksgn=='avg':
        df[ksgn]=df[zsys.ohlcLst].mean(axis=1)
    else:
        df[ksgn]=df[ksgn]
    #   xed.time
    df['xtim']=df.index
    df=df_xtim2mtim(df,'xtim',fgDate)
    #   xed.ma.xxx
    df=zta.mul_talib(zta.MA,df, ksgn,zsys.ma100Lst_var)
    #
    #   xed.xavg.xxx,predict,y_data
    df=df_xed_nextDay(df,ksgn,'x'+ksgn,10)
    #
    df=df.round(2)
    df=df.dropna()
    #
    return df
    

def df_xed_xtyp(df,kmod='3',k0=99.5,k9=100.5,sgnTyp='ktype',sgnPrice='price_change'):
    kmod=kmod.lower()
    if kmod=='n':
        df[sgnTyp]=df[sgnPrice].apply(zt.iff2ntype,v0=k0,v9=k9)                 #v0=95,v9=110)
    elif kmod=='3':   
        df[sgnTyp]=df[sgnPrice].apply(zt.iff3type,d0=k0,d9=k9,v3=3,v2=2,v1=1)   #k0=99.5,k9=100.5):
    else:    
        df[sgnTyp]=df[sgnPrice].apply(zt.iff2type,d0=k0,v1=1,v0=0)              #100.5
    #    
    df['y']=df[sgnTyp].astype(float)
    ydat=df['y'].values
    return df,ydat

#df_test['ktype']=df_test['price_change'].apply(zt.iff3type,d0=99.5,d9=100.5,v3=3,v2=2,v1=1)
    
def df_xed_xtyp2x(df_train,df_test,kmod='3',k0=99.5,k9=100.5,sgnTyp='ktype',sgnPrice='price_change'):
    df_train,y_train=df_xed_xtyp(df_train,kmod,k0,k9,sgnTyp,sgnPrice)
    df_test,y_test=df_xed_xtyp(df_test,kmod,k0,k9,sgnTyp,sgnPrice)
    #
    return df_train,df_test,y_train,y_test
    
    
#----------df.file
def df_rdcsv_tim0(fss,ksgn,tim0):
    xd0= pd.read_csv(fss,index_col=False,encoding='gbk') 
    #print('\nxd0\n',xd0.head())
    if (len(xd0)>0): 
        #xd0=xd0.sort_index(ascending=False);
        #xd0=xd0.sort_values(['date'],ascending=False);
        xd0=xd0.sort_values([ksgn],ascending=True);
        #print('\nxd0\n',xd0)
        xc=xd0.index[-1];###
        _xt=xd0[ksgn][xc];#xc=xd0.index[-1];###
        s2=str(_xt);
        #print('\nxc,',xc,_xt,'s2,',s2)
        if s2!='nan':
            tim0=s2.split(" ")[0]        
            
    #
    return xd0,tim0        

#-------------------pools

def pools_frd(rss,clst):
    print('\nclst:',clst)
    dats={}
    i,n9=0,len(clst)
    for xcod in clst:
        fcod=rss+xcod+'.csv'        
        i+=1
        print(i,'/',n9,fcod)
        df=pd.read_csv(fcod,index_col=0)
        #df=pd.read_csv(fcod)
        #
        df['avg']=df[zsys.ohlcLst].mean(axis=1).round(2)
        #
        dats[xcod]=df.sort_index()
    #
    return dats

def pools_link010(dat,pools,clst,ksgn,inxFlag=False):
    i,n9,inxSgn=0,len(clst),''
    if inxFlag:inxSgn='x'
    
    for xcod in clst:
        i+=1
        print(i,'/',n9,xcod)
        df=pools[xcod]
        #
        if ksgn=='avg':
            df['avg']=df[zsys.ohlcLst].mean(axis=1)
        #
        #print(df.tail())
        dat[inxSgn+xcod]=df[ksgn]
    #
    dat=dat.round(2)
    return dat

def pools_link2x(stkPools,clst,inxPools,xlst,ksgn):
    dat=pd.DataFrame()
    #
    dat=pools_link010(dat,stkPools,clst,ksgn)
    dat=pools_link010(dat,inxPools,xlst,ksgn,True)
    #
    return dat
    

def pools_link2qx(qx,ksgn,fgInx=True):
    dat=pd.DataFrame()
    #
    dat=pools_link010(dat,qx.stkPools,qx.stkCodeLst,ksgn)
    if fgInx:
        dat=pools_link010(dat,qx.inxPools,qx.inxCodeLst,ksgn,True)
    #
    qx.wrkPriceDat=dat
    return dat



#-------------------file

def f_links8codes(rss,clst):
    i,n9=0,len(clst)
    df9=pd.DataFrame()
    for cod in clst:
        fss=rss+cod+'.csv'
        i+=1
        print(i,'/',n9,fss)
        #
        df=pd.read_csv(fss)
        df=df[zsys.ohlcDVLst]
        df9=df9.append(df)
    #
    return df9


def f_links_TDS(rss,clst,ksgn='avg',fgDate=True):
    i,n9=0,len(clst)
    df9=pd.DataFrame()
    for cod in clst:
        fss=rss+cod+'.csv'
        i+=1
        print(i,'/',n9,fss)
        #
        df=pd.read_csv(fss)
        df=df_xed_ailib(df,ksgn,fgDate)
        df9=df9.append(df)
    #
    return df9


#-------------------file.aidat

def f_rd_xdat(fdat,xlst,ysgn='y'):
    '''
        no ysgn:'y' in xlst
    '''
    df=pd.read_csv(fdat,index_col=False)
    df['y']=df[ysgn].astype(float)
    xdat,ydat=df[xlst].values,df['y'].values
    #
    mlst=xlst+['y']
    if ysgn!='y':mlst=mlst+[ysgn]
    
    df2=df[mlst]
    #
    return df2,xdat,ydat

#-------------------file.TDS
def frd_TDS_sub(fdat,ksgn,xlst,fgChange=False):
    df=pd.read_csv(fdat)
    df['price_next']=df[zsys.xavg9Lst].max(axis=1)
    df['price'],df['y']=df[ksgn],df['price_next']
    df['price_change']=df['price_next']/df['price']*100
    if fgChange:df['y']=df['price_change']
    #
    xdat,ydat=df[xlst].values,df['y'].values
    clst,mlst=[ksgn,'y','price','price_next','price_change'],xlst
    for css in clst:
        if not (css in mlst):mlst=mlst+[css]
    #    
    df2=df[mlst]
    #
    return df2,xdat,ydat
    
def frd_TDS(rdat,fsgn,ksgn,xlst,fgChange=False):
    #rss='/ailib/TDS/'
    f_train,f_test=rdat+fsgn+'_train.csv',rdat+fsgn+'_test.csv'
    df_train,x_train,y_train=frd_TDS_sub(f_train,ksgn,xlst,fgChange)
    df_test,x_test, y_test  =frd_TDS_sub(f_test,ksgn,xlst,fgChange)
    #
    return df_train,df_test ,x_train,y_train,x_test, y_test
