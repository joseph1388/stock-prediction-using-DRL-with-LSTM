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
pd.set_option('display.float_format', zt.xfloat3)    
pyplt=py.offline.plot    
#---------------

#-----------step #1,data pre
#2 set data
print('\n#2,set data')
inxLst=['000001']
codLst=['000001','002046','600663','000792','600029','000800']
xlst=['inx','total']+codLst
tim0Str,tim9Str='2017-09-26','2017-10-18'
rs0=zsys.rdatMin0        #'/zDat/min/'
prjNam,ksgn='TM5','avg'
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
qx=zt.f_varRd(fss);#ztq.tq_prVar(qx)

#-----------step #2,BT-main

# 7       
print('\n#7 bt-main')
qx=zbt.bt_main(qx)
#
ztq.tq_prWrk(qx)
zt.prx('\nusrPools',qx.usrPools)  

#--------------
#8
print('\n#8 qx.rw')
fss=ftg0+'x2.pkl';zt.f_varWr(fss,qx)
qx=zt.f_varRd(fss);
#
#-----------step #3,ret-mini
#9
print('\n#9 ret')
#
print('\n#9.1 tq_prTrdlib')      
ztq.tq_prTrdlib(qx)
zt.prx('userPools',qx.usrPools)

print('\n#9.2 tq_usrStkMerge')      
df_usr=ztq.tq_usrStkMerge(qx)
zt.prDF('df_usr',df_usr)
#
print('\n#9.3 tq_usrDatXed')      
df2,k=ztq.tq_usrDatXed(qx,df_usr)
zt.prDF('df2',df2)
#
print('\n#9.4 ret')      
print('ret:',k,'%')

#-----------step #3,ret-all
print('\n#9.5 tq_usrDatXedFill')      
df=ztq.tq_usrDatXedFill(qx,df2)
zt.prDF('df',df)

#==============
#10 ret xed
ret=ffn.to_log_returns(df[xlst]).dropna()
ret=ffn.to_returns(df[xlst]).dropna()
ret[xlst]=ret[xlst].astype('float')
zt.prDF('\n#10,ret',ret)

#11 ret.hist
print('\n#11 ret.hist')
ax = ret.hist(figsize=(16,8))

#12
ret=ret.corr().as_format('.2f')
zt.prDF('\n#12 ret.corr',ret)

#13 
print('\n#13 calc_stats')
perf = df.calc_stats()
perf.plot()
print(perf.display())

#14
print('\n#14 r2')
ret = df.to_log_returns().dropna()
r2=ret.calc_mean_var_weights().as_format('.2%')
print(r2)
