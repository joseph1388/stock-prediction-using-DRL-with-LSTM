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

import os,sys,math,arrow,ffn
import pypinyin 
import numpy as np
import pandas as pd
import pandas_datareader as pdr 
import matplotlib.pyplot as plt
#
'''
from sklearn.datasets import samples_generator
#
import keras
from keras import initializers
from keras import models,layers
from keras.models import Sequential,load_model
from keras.layers import Dense, Input, Dropout, Embedding, LSTM, Bidirectional,Activation,SimpleRNN
from keras.optimizers import RMSprop, SGD  
from keras.applications.resnet50 import preprocess_input, decode_predictions
#
import tensorlayer as tl
import tensorflow as tf
'''
#
import zsys 
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
import ztools_draw as zdr
import ztools_tq as ztq
import zpd_talib as zta
#

#-------------------

#-------------------


#1
fss='inx/inx_code.csv'
df=pd.read_csv(fss,dtype={'code' : str},encoding='GBK')
print('\n#1,fss,',fss)
print('\ndf.tail')
print(df.tail())

#2 编辑转换数据
print('\n#2,data edit')
df2=pd.DataFrame()
for i, row in df.iterrows():
    css=row['name']
    ess=pypinyin.slug(css, style=pypinyin.FIRST_LETTER, separator='')
    row['ename']=ess.upper()+'_'+row['code']
    row['id']=int(i)
    df2=df2.append(row)
    
#3
df2['id']=df2['id'].astype(int)
fss='tmp/xinx_name.csv'
print('\n#3,fss,',fss)
df2.to_csv(fss,index=False,encoding='GBK')    
#
print('\ndf2.tail')
print(df2.tail())

