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
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    


#2
print('\n#2,读取数据')
rss,fsgn,ksgn='/ailib/TDS/','TDS2_sz50','avg'

#xlst=zsys.TDS_xlst9
xlst=zsys.TDS_xlst1
print('\nrss,fsgn,ksgn',rss,fsgn,ksgn)
print('xlst',xlst)
df_train,df_test,x_train,y_train,x_test, y_test=zdat.frd_TDS(rss,fsgn,ksgn,xlst)
#
print('\ndf_test.tail()')
print(df_test.tail())

#3
print('\n#3,数据格式')
num_x_train,num_y_train=x_train.shape[0],y_train.shape[0]
num_x_test,num_y_test=x_test.shape[0],x_test.shape[0]

print('\nnum_x_train,num_y_train:',num_x_train,num_y_train)
print('\nnum_x_test,num_y_test:',num_x_test,num_y_test)
print('\ntpye(x_train):',type(x_train))
