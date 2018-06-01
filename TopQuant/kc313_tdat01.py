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
print('\n#1fss,',fss)
df=pd.read_csv(fss,index_col=0)
df=df.sort_index(ascending=True);
print(df.tail())

#2 计算衍生参数
#2.1 计算时间衍生参数，使用ztools_data库函数
df['xtim']=df.index
df=zdat.df_xtim2mtim(df,'xtim',False)
print('\n#2.1，df.tail')
print(df.tail())
#
#2.2 计算avg均值
df['avg']=df[zsys.ohlcLst].mean(axis=1).round(2)

#
#2.3 计算ma均线数据，使用talib函数
print('\n#2.3，ma100Lst_var:',zsys.ma100Lst_var)
df=zta.mul_talib(zta.MA,df, ksgn='avg',vlst=zsys.ma100Lst_var)
#
#
#2.4 计算next次日价格，用于预测Y结果数据组
df=zdat.df_xed_nextDay(df,ksgn='avg',newSgn='xavg',nday=10)
print('\n#2，df.tail')
print(df.tail(11))
#
#2.5 
fss='tmp/stk_sum01.csv'
print('\n#2，fss',fss)
df.to_csv(fss,index=False)

#3
#计算时间参数，使用ztools_data库函数

fss='data/600663.csv'
print('\n#1fss,',fss)
df2=pd.read_csv(fss,index_col=0)


df2=zdat.df_xed_ailib(df2,'avg',True)
print('\n#3，df3.tail')
print(df2.tail(11))
#
fss='tmp/stk_sum02.csv'
print('\n#3，fss',fss)
df2.to_csv(fss,index=False)


#==========================================
''''

open,high,close,low,volume,amount,
avg,xavg,xavg_2,xavg_3,xavg_4,xavg_5,xavg_6,xavg_7,xavg_8,xavg_9
,ma_2,ma_3,ma_5,ma_10,ma_15,ma_20,ma_30,ma_50,ma_100,ma_150,ma_200,
xtim,xyear,xmonth,xday,xweekday
#,price,price_next,price_change

'''