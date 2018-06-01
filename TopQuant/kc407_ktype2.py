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

import tflearn
import tensorflow as tf

#  TopQuant
import zsys 
import zpd_talib as zta
import ztools as zt
import ztools_tq as ztq
import ztools_draw as zdr
import ztools_data as zdat

#-----------------------------

#1
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    


#2
print('\n#2,读取数据')
#fss='/zdat/cn/xday/000001.csv'
fss='data/inx_000001.csv'
df=pd.read_csv(fss,index_col=0)
df=df.sort_index()

#3
print('\n#3,整理数据')
df['xopen']=df['open'].shift(-1)
df['xclose']=df['close'].shift(-1)
print(df.tail())
#
#4
print('\n#4,数据分类')
df['kclose']=df['xclose']/df['xopen']*100
df['ktype']=df['kclose'].apply(zt.iff3type,d0=99.5,d9=101.5,v3=3,v2=2,v1=1)
#
print('df.head(100)')
print(df.head(100))
print('\ndf.tail(100)')
print(df.tail(100))


#5
print('\n#5,数据分析')
n9=len(df.index)
n3,n2,n1=sum(df['ktype']==3),sum(df['ktype']==2),sum(df['ktype']==1)
k3,k2,k1=round(n3/n9*100,2),round(n2/n9*100,2),round(n1/n9*100,2)
print('n9,',n9)
print('n3,n2,n1,',n3,n2,n1)
print('k3,k2,k1,%,',k3,k2,k1)


#9
print('\n#9,ok')


