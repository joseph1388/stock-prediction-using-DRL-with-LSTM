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
rlog='/ailib/log_tmp'
if os.path.exists(rlog):tf.gfile.DeleteRecursively(rlog)


#2
print('\n#2,读取数据')
fss='/zdat/cn/xday/000001.csv'
fss='data/inx_000001.csv'
df=pd.read_csv(fss,index_col=0)
df=df.sort_index()

#3
print('\n#3,整理数据')
cn9=df['close'].count()
df['xopen']=df['open'].shift(-1)
df1=df.head(2000)
df2=df.tail(cn9-2000)
print('\ncn9,',cn9)
print(df2.tail())
#

#4
print('\n#4,设置训练数据')
X=df1['close'].values
Y=df1['xopen'].values
print(X)
print(Y)
print(type(X))


#5
print('\n#5,构建线性回归神经网络模型')
input_ = tflearn.input_data(shape=[None])
linear = tflearn.single_unit(input_)
regression = tflearn.regression(linear, optimizer='sgd', loss='mean_square',
    metric='R2', learning_rate=0.01) 
m = tflearn.DNN(regression,tensorboard_dir=rlog)

#6
print('\n#6,开始训练模型')
m.fit(X, Y, n_epoch=100, show_metric=True, snapshot_epoch=False)


#7
print('\n#7,根据模型，进行预测')
X2=df2['close'].values
Y2=m.predict(X2)
#
ds2y=zdat.ds4x(Y2,df2.index)
df2['open2']= ds2y
#
print(df2.tail())
df2.to_csv('tmp/df2.csv')

#9
print('\n#9,ok')

