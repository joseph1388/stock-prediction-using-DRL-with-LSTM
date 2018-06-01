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

#2 rd.var
print('\n#2,rd.var')
fss='data/bt-T1x1.pkl';qx=zt.f_varRd(fss);
ztq.tq_prVar(qx)

#3
print('\n#3 set.bt.var')
qx.staFun=zsta.avg01
qx.staVars=[1.0,1.2]
#
qx.trd_buyNum=1000
qx.trd_buyMoney=10000
qx.trd_mode=1
#
qx.usrLevel,qx.trd_nilFlag=5,False
qx.usrMoney0nil=qx.usrMoney0*qx.usrLevel

# 4       
print('\n#4 bt-main')
qx=zbt.bt_main(qx)
#
ztq.tq_prWrk(qx)
zt.prx('\nusrPools',qx.usrPools)  

#--------------
#5
print('\n#5 qx.rw')
fss='tmp/bt-T1x2.pkl';zt.f_varWr(fss,qx)
#qx=zt.f_varRd(fss);#ztq.tq_prVar(qx)

#
#------------ret
#6
print('\n#6 ret')
#
print('\n#6.1 tq_prTrdlib')      
ztq.tq_prTrdlib(qx)
zt.prx('userPools',qx.usrPools)

print('\n#6.2 tq_usrStkMerge')      
df_usr=ztq.tq_usrStkMerge(qx)
zt.prDF('df_usr',df_usr)

#

print('\n#6.3 tq_usrDatXed')      
df2,k=ztq.tq_usrDatXed(qx,df_usr)
zt.prDF('df2',df2)

#
print('\n#6.4 ret')      
print('ret:',k,'%')
#==============
'''
qx.trd_nilFlag=False,
@qx.trd_mode=1
qx.trd_buyNum=1000,ret: 113.05 %
qx.trd_buyNum=3000,ret: 116.55 %
qx.trd_buyNum=5000,ret: 112.88 %
::
@qx.trd_mode=2
qx.trd_buyMoney=10000,ret: 113.64 %
qx.trd_buyMoney=30000,ret: 124.25 %
qx.trd_buyMoney=50000,ret: 121.92 %

qx.trd_nilFlag=True,qx.usrLevel=5
@qx.trd_mode=1
qx.trd_buyNum=1000,ret: 177.44 %
qx.trd_buyNum=3000,ret: 174.49 %
qx.trd_buyNum=5000,ret: 165.75 %
::
@qx.trd_mode=2
qx.trd_buyMoney=10000,ret: 179.61 %
qx.trd_buyMoney=30000,ret: 195.68 %
qx.trd_buyMoney=50000,ret: 191.54 %

'''

