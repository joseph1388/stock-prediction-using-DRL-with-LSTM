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

import os
import numpy as np
import pandas as pd
import tushare as ts

#  TopQuant
import zsys 
import zpd_talib as zta
import ztools_str as zstr
import ztools_data as zdat
import ztools_datadown as zddown

import ztools_draw as zdr

#----------

#1 读取数据
fss='data/600663.csv'
print('\n#1，fss',fss)
df=pd.read_csv(fss,index_col=0)
df=df.sort_index(ascending=True);
print(df.tail())

#2 计算时间衍生参数
#
df['xtim']=df.index
df['xyear']=df['xtim'].apply(zstr.str_2xtim,ksgn='y')
df['xmonth']=df['xtim'].apply(zstr.str_2xtim,ksgn='m')
df['xday']=df['xtim'].apply(zstr.str_2xtim,ksgn='d')
#
df['xday_week']=df['xtim'].apply(zstr.str_2xtim,ksgn='dw')
df['xday_year']=df['xtim'].apply(zstr.str_2xtim,ksgn='dy')
#df['xday_month']=df['xtim'].apply(zstr.str_2xtim,ksgn='dm')
df['xweek_year']=df['xtim'].apply(zstr.str_2xtim,ksgn='wy')
#
print('\n#2，dateLst:',zsys.dateLst)
print('\ndf.tail')
print(df.tail())


#3 计算时间衍生参数，使用ztools_data库函数
df=pd.read_csv(fss,index_col=0)
df=df.sort_index(ascending=True);
df['xtim']=df.index
df2=zdat.df_xtim2mtim(df,'xtim',True)
print('\n#3，df2.tail')
print(df2.tail())
