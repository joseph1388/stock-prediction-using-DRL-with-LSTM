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


#----------

#1
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    

#2
print('\n#2,读取数据')
fss='data/df_acc.csv'
df=pd.read_csv(fss,index_col=0)
df=df.sort_index()
print(df.tail())
df=df.dropna()

#3
print('\n#3,绘制对比曲线图')
df2=pd.DataFrame()
df2['xopen']=df['xopen']
df2['open2']=df['open2']
print(df2.tail())
df3=df2.tail(200)
df3.plot(rot=15)

#4
print('\n#4,计算预测结果')
df5=pd.DataFrame()
df5['y_test']=df2['xopen']
df5['y_pred']=df2['open2']

a1,df5x=ztq.ai_acc_xed2x(df5['y_test'],df5['y_pred'],ky0=5)
print(df5x.tail())
print('\na1,',a1)

a1,df5x,a20=ztq.ai_acc_xed2ext(df5['y_test'],df5['y_pred'],ky0=5)
print('\na20,',a20)

'''

n_df9,3671,n_dfk,3655
acc-kok: 99.56%, MAE:42.65, MSE:2463.18, RMSE:49.63
             y_test   y_pred    ysub  ysub2  y_test_div  ysubk
date                                                          
2017-04-25 3132.918 3185.180 -52.262 52.262    3132.918  1.668
2017-04-26 3131.350 3191.560 -60.210 60.210    3131.350  1.923
2017-04-27 3144.022 3203.079 -59.057 59.057    3144.022  1.878
2017-04-28 3147.228 3205.589 -58.361 58.361    3147.228  1.854
2017-05-02 3138.307 3194.470 -56.163 56.163    3138.307  1.790
a1, 99.564

n_df9,3671,n_dfk,3659
acc-kok: 99.67%, MAE:48.65, MSE:3069.45, RMSE:55.40
             y_test   y_pred   ysub  ysub2  y_test_div  ysubk
date                                                         
2017-04-25 3132.918 3070.900 62.018 62.018    3132.918  1.980
2017-04-26 3131.350 3077.054 54.296 54.296    3131.350  1.734
2017-04-27 3144.022 3088.166 55.856 55.856    3144.022  1.777
2017-04-28 3147.228 3090.588 56.640 56.640    3147.228  1.800
2017-05-02 3138.307 3079.861 58.446 58.446    3138.307  1.862
a1, 99.673
'''
