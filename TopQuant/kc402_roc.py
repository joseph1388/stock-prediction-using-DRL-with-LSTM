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
fss='data/600663.csv'
print('\n#1 fss,',fss)
df=pd.read_csv(fss,index_col=0)
df=df.sort_index(ascending=True);
print(df.tail())

#2 计算衍生参数
vlst=list(range(1,10))
print('\n#2 vlst,',vlst)
df=zta.mul_talib(zta.ROC,df, ksgn='close',vlst=zsys.ma100Lst_var)
print(df.head())
#
print('\n#3 roc01')
close_d0=df['close'][0]
close_d1=df['close'][1]
roc1=(close_d1 - close_d0)/close_d0
print('close_d0,d1:',close_d0,close_d1)
print('roc1:',roc1)


