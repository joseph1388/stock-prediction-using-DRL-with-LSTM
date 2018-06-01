# -*- coding: utf-8 -*- 
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发


网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
  
文件名:ztools_tq.py
默认缩写：import ztools_tq as ztq
简介：Top极宽量化·常用量化工具函数集
 

'''
#

import sys,os,re,pickle
import arrow,bs4,random,copy
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
import keras as ks

import sklearn
from sklearn import metrics


#
import keras
from keras.models import Sequential,load_model
from keras.utils import plot_model


#
import tflearn
import tensorflow as tf

#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat




#-------------------
#
import zpd_talib as zta

#
#-------------------




#-------init.TQ.xxx,qx.xxx


def tq_init(rs0,codLst,inxLst=['000001'],priceSgn='avg',prjNam='TQ001'):
    pd.set_option('display.width', 450)    
    pd.set_option('display.float_format', zt.xfloat3)    
    #
    qx=zsys.TQ_bar()
    qx.rdat0,qx.prjNam=rs0,prjNam
    qx.stkCodeLst,qx.inxCodeLst=codLst,inxLst
    #qx.codID,qx.codFN=xcod,zsys.rdatCN+xcod+'.csv'
    qx.priceSgn=priceSgn
    qx.priceDateFlag=(rs0.upper().find('MIN')<0)
    #
    print('tq_init name...')
    #f_stkCodNamTbl='stk_code.csv'
    fstk,finx=zsys.rdatInx+zsys.f_stkNamTbl,zsys.rdatInx+zsys.f_inxNamTbl
    qx.stkNamTbl=pd.read_csv(fstk,dtype={'code':str},encoding='GBK')
    qx.inxNamTbl=pd.read_csv(finx,dtype={'code':str},encoding='GBK')
    #
    print('tq_init pools...')
    if qx.priceDateFlag:
        qx.stkPools=zdat.pools_frd(rs0+'day/',codLst)
        qx.inxPools=zdat.pools_frd(rs0+'xday/',inxLst)
    else:
        qx.stkPools=zdat.pools_frd(rs0+'m05/',codLst)
        qx.inxPools=zdat.pools_frd(rs0+'xm05/',inxLst)
    
    print('tq_init work data...')
    if len(codLst)>0:
        xcod=qx.stkCodeLst[0]
        qx.wrkStkCod=xcod
        qx.wrkStkDat=qx.stkPools[xcod]
        qx.wrkStkInfo=qx.stkNamTbl[qx.stkNamTbl.code==xcod]
    #
    if len(inxLst)>0:
        xinx=qx.inxCodeLst[0]
        qx.wrkInxCod=xinx
        qx.wrkInxDat=qx.inxPools[xinx]
        qx.wrkInxInfo=qx.inxNamTbl[qx.inxNamTbl.code==xinx]
    #
    
    return qx



def tq_prVar(qx):
    print('\nobj:qx')
    zt.xobjPr(qx)
    #
    print('\nzsys.xxx')
    print('    rdat0,',zsys.rdat0)
    print('    rdatCN,',zsys.rdatCN)
    print('    rdatCNX,',zsys.rdatCNX)
    print('    rdatInx,',zsys.rdatInx)
    print('    rdatMin0,',zsys.rdatMin0)
    print('    rdatTick,',zsys.rdatTick)
    #
    print('\ncode list:',qx.stkCodeLst)
    print(' inx list:',qx.inxCodeLst)
    #
    zt.prx('stk info',qx.wrkStkInfo)
    zt.prx('inx info',qx.wrkInxInfo)
    zt.prx('wrkStkDat',qx.wrkStkDat.tail())
    #
    zt.prx('btTimLst',qx.btTimLst)
    zt.prx('usrPools',qx.usrPools)      #用户股票池资产数据 字典格式
    print('\nusrMoney,usrTotal:',qx.usrMoney,qx.usrTotal)    
    #
    tq_prTrdlib(qx)
    #zt.prx('qx.trdLib',qx.trdLib.head())
    #zt.prx('qx.trdLib',qx.trdLib.tail())
    #


 
def tq_prWrk(qx):
    print('\n\t bt_main_1day,',qx.wrkStkCod,qx.wrkTimStr)
    #
    zt.prx('stk info',qx.wrkStkInfo)
    zt.prx('inx info',qx.wrkInxInfo)
    zt.prx('wrkStkDat.head',qx.wrkStkDat.head(10))
    zt.prx('wrkStkDat.tail',qx.wrkStkDat.tail(10))
    #
    zt.prx('btTimLst',qx.btTimLst)
    zt.prx('usrPools',qx.usrPools)      #用户股票池资产数据 字典格式
    print('\nusrMoney,usrTotal:',qx.usrMoney,qx.usrTotal)    
    #
    #zt.prx('qx.trdLib',qx.trdLib.head())
    #zt.prx('qx.trdLib',qx.trdLib.tail())
    tq_prTrdlib(qx,30)

    
    
    
def tq_prTrdlib(qx,n9=10):
    print('\nqx.trdLib')
    dfq,nc=qx.trdLib,0
    dfq=dfq.round(3)
    print('\ttime,\tID,\tcash,\t\tusrPools')
    for xc,row in dfq.iterrows():
        nc+=1
        if nc<n9:
            upools=row['upools']
            xss='{0},{1},${2:0.2f}'.format(row['time'],row['ID'],row['cash'])
            print(xss,'\t',upools)
    #            
    dn9=len(dfq.index)
    if dn9>n9:
        print('......')
        nc0,nc=dn9-n9,0
        for xc,row in dfq.iterrows():
            nc+=1
            if nc>nc0:
                upools=row['upools']
                xss='{0},{1},${2:0.2f}'.format(row['time'],row['ID'],row['cash'])
                print(xss,'\t',upools)
    #
    print('\nn-trdlib：',dn9)

#-------tq.pools.xxxx
    
def tq_pools_wr(qx):
    fss=qx.rtmp+qx.wrkStkCod+'.csv'
    qx.wrkStkDat.to_csv(fss)
    
    
        
def tq_pools_chk(qx):
    print('\n@tq_pools_chk,xcode',qx.wrkStkCod)
    print(qx.wrkStkDat.tail())
    
def tq_pools_call(qx,xfun):
    for xcod in qx.stkCodeLst:
        qx.wrkStkCod=xcod
        qx.wrkStkDat=qx.stkPools[xcod]
        #sta_dataPre(qx)
        xfun(qx)
        qx.stkPools[xcod]=qx.wrkStkDat
        #
        #print('\ntq_pools_call,',xcod)
        #print(qx.stkPools[xcod].tail())
    #
    return qx
    


#---------------tq.trd.xxx

    

    
        
#---------------------------tq.stk.xxx
def tq_stkGetPrice(df,ksgn,xtim):
    '''
      获取当前价格
    
    Args:
        qx (zwQuantX): zwQuantX交易数据包
        ksgn (str): 价格模式代码
        '''
    #d10=dfw.stkLib[qx.stkCode]
    d01=df[xtim:xtim];
    #
    price=0;
    if len(d01)>0:
        d02=d01[ksgn]
        price=d02[0];
        if pd.isnull(price):
            d02=d01['dprice']
            price=d02[0];
    #
    price=round(price,3)
    return price

#---------------------------stk

def stk2data_pre8FN(fss):
    if not os.path.exists(fss):
        return None
    #    
    df=pd.read_csv(fss,index_col=0)
    df['avg']=df[zsys.ohlcLst].mean(axis=1)
    #
    df['avg']=df[zsys.ohlcLst].mean(axis=1)
    df,avg_lst=zdat.df_xshift(df,ksgn='avg',num9=10)
    #print('avg_lst,',avg_lst)
    #
    mv_lst=[2,3,5,10,15,20,30,50,100,150,200]
    #ma_lst=[2,3,4,5,6,7,8,9,10,15,20,30,40,50,60,80,100,120,150,180,200,250,300]
    df=zta.mul_talib(zta.MA,df, ksgn='avg',vlst=mv_lst)
    ma_lst=zstr.sgn_4lst('ma',mv_lst)
    #
    df['xtim']=df.index
    df['xyear']=df['xtim'].apply(zstr.str_2xtim,ksgn='y')
    df['xmonth']=df['xtim'].apply(zstr.str_2xtim,ksgn='m')
    df['xday']=df['xtim'].apply(zstr.str_2xtim,ksgn='d')
    df['xweekday']=df['xtim'].apply(zstr.str_2xtim,ksgn='w')
    tim_lst=['xyear','xmonth','xday','xweekday']
    #
    df['price']=df['avg']
    df['price_next']=df[avg_lst].max(axis=1)
    #涨跌幅,zsys.k_price_change=1000
    df['price_change']=df['price_next']/df['price']*100
    #df['ktype']=df['price_change'].apply(zt.iff2type,d0=100)  
    #def dat2type(d,k9=2000,k0=0):
    #fd>120
    #
    df=df.dropna()
    #df['ktype']=round(df['price_change']).astype(int)
    #df['ktype']=df['kprice'].apply(zt.iff2type,d0=100)  
    #df['ktype']=df['price_change'].apply(zt.iff3type,v0=95,v9=105,v3=3,v2=2,v1=1)  
    #
    df=df.round(3)
    return df


    
def stk2data_pre8Flst(finx,rss):
    flst=pd.read_csv(finx,index_col=False,dtype='str',encoding='gbk')
    df9=pd.DataFrame()
    xc=0
    for xcod in flst['code']:
        #print(xcod)
        xc+=1
        fss=rss+xcod+'.csv';print(xc,'#',fss)
        df=stk2data_pre8FN(fss)
        df9=df9.append(df)
    #
    return df9

#---------------------------user.xxx
def tq_usrIDSet(qx):
    ''' 生成订单流水号编码ID
       #ID=prjName+'_'+trdCnt(000000)
    '''

    qx.trdCnt+=1;
    nss='{:05d}'.format(qx.trdCnt);
    qx.trdID=qx.prjNam+'_'+nss;
    #

    return qx.trdID   

#---------------------------user.pools

def tq_usrPoolsMerge(qx):
    #inx_cod,ksgn=qx.inxCodeLst[0],qx.priceSgn
    #df_inx=qx.inxPools[inx_cod]
    ksgn=qx.priceSgn
    df9=pd.DataFrame()
    for xcod in qx.inxCodeLst:
        df=qx.inxPools[xcod]
        df9['x'+xcod]=df[ksgn]
    #
    for xcod in qx.stkCodeLst:
        df=qx.stkPools[xcod]
        df9[xcod]=df[ksgn]
    #
    return df9


def tq_usrPoolsAdd(upools,xcod,ksgn,dat):
    usr1=upools.get(xcod)
    if usr1==None:usr1={}
    v=tq_usrPoolsGet(upools,xcod,ksgn)
    #
    usr1[ksgn]=round(v+dat,2)
    #
    upools[xcod]=usr1
    #print(v,v+dat,'v',xcod,ksgn,dat)
    #
    return upools

def tq_usrPoolsGet(upools,xcod,ksgn):
    v,usr1=0,upools.get(xcod)
    #print('v,usr1',v,usr1,xcod,upools)
    if usr1!=None:v=usr1.get(ksgn)
    #print('v,usr2',v,usr1)
    if v==None:v=0
    #print('v,usr3',v,usr1)
    #if ksgn!='code':
    v=round(v,3)
    #
    return v

def tq_usrPoolsPut(upools,xcod,ksgn,dat):
    usr1=upools.get(xcod)
    if usr1==None:usr1={}
    #
    usr1[ksgn]=round(dat,3)
    upools[xcod]=usr1
    #
    return upools


def tq_usrPoolsPutAll(upools,xcod,num9,dnum):
    #tq_usrPoolsPut(upools,xcod,'code',xcod)
    tq_usrPoolsPut(upools,xcod,'num9',num9)
    #tq_usrPoolsPut(upools,xcod,'sum',sum9)
    tq_usrPoolsPut(upools,xcod,'dnum',dnum)
    #tq_usrPoolsPut(upools,xcod,'dsum',dsum)
    #tq_usrPoolsPut(upools,xcod,'dprice',dprice)
    #
    return upools
        

def tq_usrPoolsInit(qx,addFg=False):
    upools=qx.usrPools
    for xcod in qx.stkCodeLst:
        num9=0
        if addFg:num9=tq_usrPoolsGet(upools,xcod,'num9')
        #
        tq_usrPoolsPutAll(upools,xcod,num9,0)
    #
    qx.usrPools=upools
    return qx

def tq_usr2trdLib(qx):
    xtim,upools=qx.wrkTimStr,qx.usrPools
    r1=pd.Series(zsys.qx_trdNil,index=zsys.qx_trdName);
    #
    r1['ID']=tq_usrIDSet(qx)
    r1['time'],r1['cash']=xtim,qx.usrMoney
    #r1['upools']=qx.usrPools.copy()
    r1['upools']=copy.deepcopy(upools)
    #
    qx.trdLib=qx.trdLib.append(r1.T,ignore_index=True)
    
  
    #

#---------------------------user.stk

def tq_usrStkMerge(qx):
    inx_cod,ksgn=qx.inxCodeLst[0],qx.priceSgn
    df_inx,dfq=qx.inxPools[inx_cod],qx.trdLib
    dfq.index=dfq['time']
    #zt.prx('dfq',dfq)
    #
    df9=pd.DataFrame()
    df9['inx'],df9['cash'],df9['total']=df_inx[ksgn],dfq['cash'],0
    df9=df9.dropna()
    #zt.prDF('df9',df9)
    for xcod in qx.stkCodeLst:
        df=qx.stkPools[xcod]
        df9[xcod]=df[ksgn]
    #
    return df9

def tq_usrDatXed(qx,dfu):
    df2=zdat.df_kcut8tim(dfu,'',qx.btTim0Str,qx.btTim9Str)
    #
    clst=qx.stkCodeLst
    nlst=list(map(lambda x:x+'_num',clst))
    mlst=list(map(lambda x:x+'_money',clst))
    dlst=list(df2.columns);#+['stk-val']
    xlst=dlst+nlst+mlst; #print('xlst',xlst)
    #
    df3=pd.DataFrame(columns=xlst)
    df3[dlst]=df2
    #
    dfq=qx.trdLib
    dfq=zdat.df_kcut8tim(qx.trdLib,'',qx.btTim0Str,qx.btTim9Str)
    #dfq=dfq[dfq.index>=qx.btTim0St]
    #dfq=dfq[dfq.index<=qx.btTim9Str]
    #
    for xsgn in nlst:
        dfq[xsgn]=0
    #        
    for xtim,row in dfq.iterrows():
        upools=row['upools']
        #print(xtim,'#',upools)
        for xcod in upools:
            xnum=tq_usrPoolsGet(upools,xcod,'num9')
            df3.ix[xtim,xcod+'_num']=xnum
            #
    #
    
    df3=df3.fillna(method='pad')
    #
    for xcod in clst:
        mss,nss=xcod+'_money',xcod+'_num'
        df3[mss]=df3[xcod]*df3[nss]
    #
    df3['stk-val']=df3[mlst].sum(axis=1)
    df3['total']=df3['stk-val']+df3['cash']
    #
    #
    #print('df3.tail()')
    #print(df3.tail())
    x=df3.tail(1)
    x2=x['total'].values[0]
    k=round(x2/qx.usrMoney0*100,2)
    #
    return df3,k

   

    

def tq_usrDatXedFill(qx,dfu):
    #df2=zdat.df_kcut8tim(dfu,'',qx.btTim0Str,qx.btTim9Str)
    #df2=dfu[dfu.index>=tim0Str]
    #df2=df2[df2.index<=tim9Str]
    #print('df2.tail()')
    #print(df2.tail())
    #
    #xcod=qx.wrkInxCod
    #df=qx.inxPools[xcod]
    #
    df9=pd.DataFrame()
    clst=qx.stkCodeLst
    mlst=list(map(lambda x:x+'_money',clst))
    #
    #df=qx.wrkInxDat
    ksgn=qx.priceSgn
    df9['inx']=qx.wrkInxDat[ksgn]
    df9['cash']=dfu['cash']
    #
    for xcod in clst:
        nss,mss=xcod+'_num',xcod+'_money'
        #nss=xcod+'_num'
        #df9[xcod],df9[nss],df9[mss]=dfu[xcod],dfu[nss],dfu[mss]
        df=qx.stkPools[xcod]
        df9[xcod],df9[nss]=df[ksgn],dfu[nss]
        df9[mss]=df9[xcod]*df9[nss]
        
    #
    df9=df9.fillna(method='pad')
    df9[mss]=df9[xcod]*df9[nss]
    df9['stk-val']=df9[mlst].sum(axis=1)
    df9['total']=df9['stk-val']+df9['cash']    
    #
    df9=zdat.df_kcut8tim(df9,'',qx.btTim0Str,qx.btTim9Str)
    #
    xlst=['inx','total']+clst
    #df9[xlst]=df9[xlst]
    df=df9[xlst]
    df.index=pd.DatetimeIndex(df.index)
    #
    return df
    
#------------    
    
#---------------------------tick    

def tick2x(df,ktim='1min'):
    '''
    ktim，是时间频率参数，请参看pandas的resample重新采样函数
        常见时间频率符号： 
            A， year 
            M， month 
            W， week 
            D， day 
            H， hour 
            T， minute 
            S，second
    '''
    #
    df['time']=pd.to_datetime(df['time']) 
    df=df.set_index('time')
    df=df.sort_index()
    #
    dfk=df['price'].resample(ktim).ohlc();dfk=dfk.dropna();
    vol2=df['volume'].resample(ktim).sum();vol2=vol2.dropna();
    df_vol2=pd.DataFrame(vol2,columns=['volume'])
    amt2=df['amount'].resample(ktim).sum();amt2=amt2.dropna();
    df_amt2=pd.DataFrame(amt2,columns=['amount'])
    #
    df2=dfk.merge(df_vol2,left_index=True,right_index=True)
    df9=df2.merge(df_amt2,left_index=True,right_index=True);
    #
    xtims=df9.index.format('%Y-%m-%d %H:%M:%S')
    del(xtims[0])
    df9['xtim']=xtims # df9.index.__str__();#  [str(df9.index)]
    #             
    return df9    


#---------------------------ai.xxx
def ai_varRd(fmx0):
    fvar=fmx0+'tqvar.pkl'
    qx=zt.f_varRd(fvar)
    for xkey in qx.aiMKeys:
        fss=fmx0+xkey+'.mx'
        mx=load_model(fss)
        qx.aiModel[xkey]=mx
    #
    return qx
    
def ai_varWr(qx,fmx0):    
    fvar=fmx0+'tqvar.pkl'
    mx9=qx.aiModel
    qx.aiMKeys=list(mx9.keys())
    qx.aiModel={}
    zt.f_varWr(fvar,qx)
    print('fvar,',fvar)
    #
    for xkey in mx9:
        fss=fmx0+xkey+'.mx'
        mx9[xkey].save(fss)
        print('fmx,',fss)
    #
    qx.aiModel=mx9
    
#---------------------------ai.xxx
    
#---------------------------ai.dacc
def ai_acc_xed2x(y_true,y_pred,ky0=5,fgDebug=False):
    '''
    效果评估函数，用于评估机器学习算法函数的效果。
    输入：
    	y_true,y_pred，pandas的Series数据列格式。
    	ky0，结果数据误差k值，默认是5，表示百分之五。
    	fgDebug，调试模式变量，默认为False。
    返回：
        dacc,准确率，float格式
        df，结果数据，pandas列表格式DataFrame
    
    '''
    #1
    df,dacc=pd.DataFrame(),-1
    #print('n,',len(y_true),len(y_pred))
    if (len(y_true)==0) or (len(y_pred)==0):
        #print('n,',len(y_true),len(y_pred))
        return dacc,df
        
    #
    y_num=len(y_true)
    #df['y_true'],df['y_pred']=zdat.ds4x(y_true,df.index),zdat.ds4x(y_pred,df.index)
    df['y_true'],df['y_pred']=pd.Series(y_true),pd.Series(y_pred)
    df['y_diff']=np.abs(df.y_true-df.y_pred)
    #2
    df['y_true2']=df['y_true']
    df.loc[df['y_true'] == 0, 'y_true2'] =0.00001
    df['y_kdif']=df.y_diff/df.y_true2*100
    #3
    dfk=df[df.y_kdif<ky0]   
    knum=len(dfk['y_pred'])
    dacc=knum/y_num*100
    #
    #5
    dacc=round(dacc,3)
    return dacc,df

def ai_acc_xed2ext(y_true,y_pred,ky0=5,fgDebug=False):
    '''
    效果评估函数，用于评估机器学习算法函数的效果。
    输入：
    	y_true,y_pred，pandas的Series数据列格式。
    	ky0，结果数据误差k值，默认是5，表示百分之五。
    	fgDebug，调试模式变量，默认为False。
    返回：
        dacc,准确率，float格式
        df，结果数据，pandas列表格式DataFrame
        [dmae,dmse,drmse,dr2sc]，各种扩充评估数据
    
    '''    
    #1
    df,dacc=pd.DataFrame(),-1
    if (len(y_true)==0) or (len(y_pred)==0):
        #print('n,',len(y_true),len(y_pred))
        return dacc,df
        
    #2
    y_num=len(y_true)
    #df['y_true'],df['y_pred']=zdat.ds4x(y_true,df.index),zdat.ds4x(y_pred,df.index)
    df['y_true'],df['y_pred']=y_true,y_pred
    df['y_diff']=np.abs(df.y_true-df.y_pred)
    #3
    df['y_true2']=df['y_true']
    df.loc[df['y_true'] == 0, 'y_true2'] =0.00001
    df['y_kdif']=df.y_diff/df.y_true2*100
    #4
    dfk=df[df.y_kdif<ky0]   
    knum=len(dfk['y_pred'])
    dacc=knum/y_num*100
    #
    #5
    dmae=metrics.mean_absolute_error(y_true, y_pred)
    dmse=metrics.mean_squared_error(y_true, y_pred)
    drmse=np.sqrt(metrics.mean_squared_error(y_true, y_pred))
    dr2sc=metrics.r2_score(y_true,y_pred)
    #    
    #6
    if fgDebug:
        #print('\nai_acc_xed')
        #print(df.head())
        #y_test,y_pred=df['y_test'],df['y_pred']
        print('ky0={0}; n_df9,{1},n_dfk,{2}'.format(ky0,y_num,knum))
        print('acc: {0:.2f}%;  MSE:{1:.2f}, MAE:{2:.2f},  RMSE:{3:.2f}, r2score:{4:.2f}, @ky0:{5:.2f}'.format(dacc,dmse,dmae,drmse,dr2sc,ky0))
        
    #
    #7
    dacc=round(dacc,3)
    xlst=[dmae,dmse,drmse,dr2sc]
    return dacc,df,xlst

#---------------------------ai.model.xxx    
def ai_mul_var_tst(mx,df_train,df_test,nepochs=200,nsize=128,ky0=5):
    x_train,y_train=df_train['x'].values,df_train['y'].values
    x_test, y_test = df_test['x'].values,df_test['y'].values
    #
    mx.fit(x_train, y_train, epochs=nepochs, batch_size=nsize)
    #
    y_pred = mx.predict(x_test)
    df_test['y_pred']=zdat.ds4x(y_pred,df_test.index,True)
    dacc,_=ai_acc_xed2x(df_test.y,df_test['y_pred'],ky0,False)
    #
    return dacc
    

def ai_mx_tst_epochs(f_mx,f_tg,df_train,df_test,kepochs=100,nsize=128,ky0=5):
    ds,df={},pd.DataFrame()
    for xc in range(1,11):
        print('\n#',xc)
        dnum=xc*kepochs
        mx=ks.models.load_model(f_mx)
        t0=arrow.now()
        dacc=ai_mul_var_tst(mx,df_train,df_test,dnum,nsize,ky0=ky0)
        tn=zt.timNSec('',t0)
        ds['nepoch'],ds['epoch_acc'],ds['ntim']=dnum,dacc,tn
        df=df.append(ds,ignore_index=True)    
        
    #
    df=df.dropna()
    df['nepoch']=df['nepoch'].astype(int)
    print('\ndf')
    print(df)
    print('\nf,',f_tg)
    df.to_csv(f_tg,index=False)
    #
    df.plot(kind='bar',x='nepoch',y='epoch_acc',rot=0)
    df.plot(kind='bar',x='nepoch',y='ntim',rot=0)
    #
    return df



def ai_mx_tst_bsize(f_mx,f_tg,df_train,df_test,nepochs=500,ksize=32,ky0=5):
    ds,df={},pd.DataFrame()
    for xc in range(1,11):
        print('\n#',xc)
        dnum=xc*ksize
        mx=ks.models.load_model(f_mx)
        t0=arrow.now()
        dacc=ai_mul_var_tst(mx,df_train,df_test,nepochs,dnum,ky0=ky0)
        tn=zt.timNSec('',t0)
        ds['bsize'],ds['size_acc'],ds['ntim']=dnum,dacc,tn
        df=df.append(ds,ignore_index=True)    
        
    #
    df=df.dropna()
    df['bsize']=df['bsize'].astype(int)
    print('\ndf')
    print(df)
    print('\nf,',f_tg)
    df.to_csv(f_tg,index=False)
    #
    df.plot(kind='bar',x='bsize',y='size_acc',rot=0)
    df.plot(kind='bar',x='bsize',y='ntim',rot=0)
    return df

    
def ai_mx_tst_kacc(f_mx,f_tg,df_train,df_test,nepochs=500,nsize=128):
    ds,df={},pd.DataFrame()
    for xc in range(1,11):
        print('\n#',xc)
        dnum=xc*1
        mx=ks.models.load_model(f_mx)
        dacc=ai_mul_var_tst(mx,df_train,df_test,nepochs,nsize,ky0=dnum)
        ds['kacc'],ds['dacc']=dnum,dacc
        df=df.append(ds,ignore_index=True)    
        
    #
    df=df.dropna()
    df['kacc']=df['kacc'].astype(int)
    print('\ndf')
    print(df)
    print('\nf,',f_tg)
    df.to_csv(f_tg,index=False)
    #
    df.plot(kind='bar',x='kacc',y='dacc',rot=0)
    #
    return df

    

    