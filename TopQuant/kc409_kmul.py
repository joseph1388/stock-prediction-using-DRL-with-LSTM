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
import pandas as pd
import numpy as np
import tflearn
import tensorflow as tf
#
import ztools as zt
import ztools_data as zdat

#
import zsys
import ztools_tq as ztq

#------------------

#1
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    
rlog='/ailib/log_tmp'
if os.path.exists(rlog):tf.gfile.DeleteRecursively(rlog)



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
df['kclose']=df['xclose']/df['xopen']*100
df['ktype']=df['kclose'].apply(zt.iff3type,d0=99.5,d9=101.5,v3=3,v2=2,v1=1)
df['ktype']=df['ktype']-1
#


#4
print('\n#4,设置训练数据')
n9=len(df.index)
df1=df.head(2000)
df2=df.tail(n9-2000)
#
X=df1[zsys.ohlcLst].values
Y=df1['ktype'].values
y1s=pd.get_dummies(Y)
y1=y1s.values
#

#5
print('\n#5,构建线性回归神经网络模型')
net = tflearn.input_data(shape=[None, 4])
#net = tflearn.fully_connected(net, 40)
net = tflearn.fully_connected(net, 40)
net = tflearn.fully_connected(net, 3, activation='softmax')
net = tflearn.regression(net)
#
m = tflearn.DNN(net,tensorboard_dir=rlog)
#
#6
print('\n#6,开始训练模型')
m.fit(X, y1, n_epoch=100, show_metric=True)

#7
print('\n#7,根据模型，进行预测')
X2=df2[zsys.ohlcLst].values
Y2=m.predict(X2)
#
y2v=map(np.argmax,Y2)
ds2y=zdat.ds4x(y2v,df2.index)
df2['ktype2']= ds2y
#
print(df2.tail())
df2.to_csv('tmp/df2.csv')
#
#8
print('\n#8,计算预测结果')
df5=pd.DataFrame()
df5['y_test']=df2['ktype']
df5['y_pred']=df2['ktype2']
acc,df5x=ztq.ai_acc_xed2x(df5['y_test'],df5['y_pred'],ky0=0.5)
#
print('\nacc,',acc)
print(df5.tail())
df5.to_csv('tmp/df5.csv')

#9
print('\n#9,ok')


