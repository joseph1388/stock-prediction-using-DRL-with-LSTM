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

import os,ffn
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
import ztools_draw as zdr
import ztools_data as zdat


#----------
#1set data 
vlst=['sz50','hs300','zz500']
vss=vlst[2]
#vss='003'
#
rss=zsys.rdatCN     #/zdat/cn/day/
ftg='tmp/TDS20_'+vss+'.csv'
ftg_rnd='tmp/TDS2_'+vss+'.csv'
ftg_train='tmp/TDS2_'+vss+'_train.csv'
ftg_test='tmp/TDS2_'+vss+'_test.csv'


#
finx='inx/stk_'+vss+'.csv'
df=pd.read_csv(finx,dtype={'code' : str},encoding='GBK')
print('\n#1 finx,',finx,ftg)
#
#2 TDS link data
xlst=list(df['code'])
print('\n#2xlst,',xlst)
df9=zdat.f_links_TDS(rss,xlst,'avg',True)
#
print(df9.tail())
print(ftg)
df9.to_csv(ftg,index=False)


#3 rnd
df9.drop('xtim',axis=1, inplace=True)
#df9=df9.sample(frac=1.0)
print(df9.tail())
print(ftg_rnd)
df9.to_csv(ftg_rnd,index=False)

#4  cut:trian,test
n9=len(df9.index)
ktim='2017-01-01'
df_train=df9[df9.date<ktim]
df_test=df9[df9.date>=ktim]

num_train,num_test=len(df_train.index),len(df_test.index)
print('\nnum_train,num_test,',num_train,num_test)
#
print('\ndf_train.tail()')
print(df_train.tail())
df_train.to_csv(ftg_train,index=False)

print('\ndf_test.tail()')
print(df_test.tail())
df_test.to_csv(ftg_test,index=False)

