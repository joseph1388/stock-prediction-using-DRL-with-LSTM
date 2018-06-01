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
import ztools_str as zstr
import ztools_draw as zdr
import ztools_data as zdat



#----------

#1
rss=zsys.r_TDS
#fss='data/600663.csv'
fss=rss+'TDS_sz50.csv'
print('\n#1fss,',fss)
df=pd.read_csv(fss,index_col=0)
print(df.tail())
#
#
#2 计算衍生参数
print('\n#x2 data edit')
vlst=list(range(1,10))
xlst=zstr.sgn_4lst('xavg',vlst,'')
print('xlst:',xlst)

ksgn='avg'
df['price']=df[ksgn]
df['price_next']=df[xlst].max(axis=1)
df['price_change']=df['price_next']/df['price']*100
#

#3.1, 1 in 2
print('\n#3.1, 1 in 2')
df['ktype2']=df['price_change'].apply(zt.iff2type,d0=101,v1=1,v0=0)  
print('\ndf.tail')
print(df.tail(10))
print(df['ktype2'].value_counts())

#3.2, 1 in 3
print('\n#3.2, 1 in 3')
df['ktype3']=df['price_change'].apply(zt.iff3type,d0=95,d9=105,v3=3,v2=2,v1=1)
print('\ndf.tail')
print(df.tail(10))
print(df['ktype3'].value_counts())


#3.3, ntype
print('\n#3.2, 1 in 3')
df['ktype_n']=df['price_change'].apply(zt.iff2ntype,v0=95,v9=105)  
print('\ndf.tail')
print(df.head(20))
print(df['ktype_n'].value_counts())
ds=df['ktype_n'].value_counts()
ds.plot(kind='bar')

