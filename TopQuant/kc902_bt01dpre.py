# -*- coding: utf-8 -*-
'''
TopQuant-简称TQ极宽智能量化回溯分析系统，培训课件-配套教学python课件程序

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2017.10.1 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
'''

import os,arrow,ffn,pickle
import numpy as np
import pandas as pd
import tushare as ts

import plotly as py
import plotly.figure_factory  as pyff

#  TopQuant
import zsys 
import zpd_talib as zta
import ztools as zt
import ztools_tq as ztq
import ztools_bt as zbt
import ztools_sta as zsta
import ztools_str as zstr
import ztools_data as zdat
import ztools_datadown as zddown
import ztools_draw as zdr



#-------------------    

#1 预处理
pd.set_option('display.width', 450)    
pyplt=py.offline.plot    
#---------------

#2 set data
print('\n#2,set data')
inxLst=['000001']
codLst=['000001','002046','600663','000792','600029','000800']
tim0Str,tim9Str='2017-01-01','2017-09-30'
rs0=zsys.rdatCN0        #'/zDat/cn/'
prjNam,ksgn='T1','avg'
ftg0='tmp/'+prjNam
print('rs0,',rs0)


#3 init.qx
print('\n#3,init.qx')
qx=zbt.bt_init(rs0,codLst,inxLst,tim0Str,tim9Str,ksgn,prjNam)
ztq.tq_prVar(qx)

#
#4 set.bT.var
print('\n#4,set.BT.var')
qx.preFun=zsta.avg01_dpre
qx.preVars=[10]
qx.staFun=zsta.avg01
qx.staVars=[1.1,1.1]
#
#5 set.bT.var
print('\n#5,call::qx.preFun')
ztq.tq_pools_call(qx,qx.preFun)

#6 save.var
print('\n#6,save.var')
fss=ftg0+'x1.pkl';zt.f_varWr(fss,qx)
qx=zt.f_varRd(fss);
ztq.tq_prVar(qx)

#------------
#7 chk.dat
print('\n7.1 tq_pools_chk')
ztq.tq_pools_call(qx,ztq.tq_pools_chk)

print('\n#7.2,plot inx -->tmp/tmp_.html')
xinx,df=qx.wrkInxCod,qx.wrkInxDat
hdr,fss='k线图-inx '+xinx,'tmp/tmp_'+xinx+'.html'
df2=df.tail(100)
zdr.drDF_cdl(df2,ftg=fss,m_title=hdr)

print('\n#7.3,plot stk-->tmp/tmp_.html')
xcod,df=qx.wrkStkCod,qx.wrkStkDat
hdr,fss='k线图-stk '+xcod,'tmp/tmp_'+xcod+'.html'
df2=df.tail(100)
zdr.drDF_cdl(df2,ftg=fss,m_title=hdr)

#8
print('\n#8.1,stk.merge')
df9=ztq.tq_usrPoolsMerge(qx)

print('\n#8.2,dat,cut')
df2=zdat.df_kcut8tim(df9,'',tim0Str,tim9Str)
zt.prDF('\n#df2',df2)
        
print('\n#8.3,rebase')        
dfx=df2.rebase()
zt.prDF('\n#dfx',dfx)
        
print('\n#8.4,plot,rebase')
dfx.plot()
