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
#1
print('\n#1,init ')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat5)    

    


#2
print('\n#2,set.dat')
df=pd.read_csv('data/002046.csv')
df=df.sort_values('date')

#3
print('\n#3,set.new dat')
df['xopen']=df['open'].shift(-1)


#4
print('\n#4,corr')
df['kopen']=df['xopen'].corr(df['open'])
df['khigh']=df['xopen'].corr(df['high'])
df['klow']=df['xopen'].corr(df['low'])
df['kclose']=df['xopen'].corr(df['close'])

print(df.tail())

#5
print('\n#5,describe')
print(df.describe())

#6
print('\n#6,ok')
