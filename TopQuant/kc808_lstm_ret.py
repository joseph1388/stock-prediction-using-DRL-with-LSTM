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
#2
import keras
from keras import initializers,models,layers
from keras.models import Sequential,load_model
from keras.layers import Flatten,Dense, Input, Dropout, Embedding,SimpleRNN,Bidirectional,LSTM,Conv1D, GlobalMaxPooling1D,Activation,MaxPooling1D,GlobalAveragePooling1D
from keras.optimizers import RMSprop
from keras.utils import plot_model

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


#2 set data
codLst=['000001','002046','600663','000792','600029','000800']
xlst=['inx','total']+codLst
#
print('\n#2.2 qx.rd')
fss='data/TM2_tqvar.pkl';qx=zt.f_varRd(fss)

#3
print('\n#3.1 tq_usrStkMerge')      
df_usr=ztq.tq_usrStkMerge(qx)
zt.prDF('df_usr',df_usr)

print('\n#3.2 tq_usrDatXed')      
df2,k=ztq.tq_usrDatXed(qx,df_usr)
zt.prDF('df2',df2)
#
print('\n#3.3 ret')      
print('ret:',k,'%')

print('\n#3.4 tq_usrDatXedFill')      
df=ztq.tq_usrDatXedFill(qx,df2)
zt.prDF('df',df)

#==============
#4 ret xed
ret=ffn.to_log_returns(df[xlst]).dropna()
zt.prDF('\n#4.1,ret#1',ret)
#
ret=ffn.to_returns(df[xlst]).dropna()
zt.prDF('\n#4.2,ret#2',ret)
#
ret[xlst]=ret[xlst].astype('float')
zt.prDF('\n#4.3,ret#3',ret)

#5 ret.hist
print('\n#5 ret.hist')
ax = ret.hist(figsize=(16,8))

#6
print('\n# ret.corr()')
ret=ret.corr().as_format('.2f')
zt.prDF('\n#6 ret.corr',ret)

#7
print('\n#7 rebase')
df2=df.rebase()
ax = df2.plot()
zt.prDF('\n#7 rebase',df2)
        
#8 
print('\n#8.1 calc_stats')
perf = df.calc_stats()
perf.plot()
print(perf.display())

#8
xcod='002046'
print('\n#8.2 display_monthly_return')
m1=perf[xcod].display_monthly_returns()
print(m1)

print('\n#8.3 xcod.stats')
m2=perf[xcod].stats
print(m2)

#9
print('\n#9 r2')
ret = df.to_log_returns().dropna()
r2=ret.calc_mean_var_weights().as_format('.2%')
print(r2)
