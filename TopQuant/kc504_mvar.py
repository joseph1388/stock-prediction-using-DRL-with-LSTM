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
#
import keras
from keras.models import Sequential,load_model
from keras.layers import Dense, Input, Dropout
from keras.optimizers import RMSprop
from keras.utils import plot_model
#
import tensorlayer as tl
import tensorflow as tf
#
#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
import ztools_draw as zdr
import ztools_tq as ztq
import zpd_talib as zta
#



#------------------
 
#1
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    
rlog='/ailib/log_tmp'
if os.path.exists(rlog):tf.gfile.DeleteRecursively(rlog)

#2
print('\n#2,读取数据')
fss='data/lin_reg2.csv'
df=pd.read_csv(fss)
print('f,',fss)
print(df.tail())
#
#3
print('\n#3,xed.train.数据')
dnum=len(df.index)
dnum2=round(dnum*0.6)
print('\ndnum,',dnum,dnum2)
df_train=df.head(dnum2)
df_test=df.tail(dnum-dnum2)
#
x_train,y_train=df_train['x'].values,df_train['y'].values
x_test, y_test = df_test['x'].values,df_test['y'].values
#print('train,',x_train[0],y_train[0])
print('type,',type(x_train),type(y_train))
print('shape,',x_train.shape,y_train.shape)

#------------------
#
    
#4
fmx='data\mlp01.dat'
ftg='tmp/df5.csv'    
#
df2=ztq.ai_mx_tst_epochs(fmx,ftg,df_train,df_test,kepochs=100,nsize=128,ky0=5)
#df2=ztq.ai_mx_tst_bsize(fmx,ftg,df_train,df_test,nepochs=300,ksize=8,ky0=5)
#df2=ztq.ai_mx_tst_kacc(fmx,ftg,df_train,df_test,nepochs=300,nsize=128)

