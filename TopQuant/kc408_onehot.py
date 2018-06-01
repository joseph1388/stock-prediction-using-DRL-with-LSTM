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


#2
print('\n#2,读取数据')
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
print(df.tail())

#4
print('\n#4,设置训练数据')
n9=len(df.index)
df1=df.head(2000)
df2=df.tail(n9-2000)
#
X=df1[zsys.ohlcLst].values
Y=df1['ktype'].values

#5
print('\n#5,One-Hot Encode')
y_onehot=pd.get_dummies(Y)
print('y_onehot.head(5)')
print(y_onehot.head(5))
y1s=pd.get_dummies(y_onehot)
print('y1s.head(5)')
print(y1s.head(5))
#
y1=y1s.values
print('y1')
print(y1)
print('type(y1),',type(y1))
print('y1.shape,',y1.shape)
#
#6
print('\n#6,One-Hot Decode')
a0,a1=y1[0],y1[1]
a0v,a1v=np.argmax(a0,axis=0),np.argmax(a1,axis=0)
print('\na0v,',a0v,a0)
print('a1v,',a1v,a1)

