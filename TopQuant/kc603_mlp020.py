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
#1
import os,arrow
import pandas as pd
import numpy as np
#2
import keras
from keras import initializers,models,layers
from keras.models import Sequential
from keras.layers import Flatten,Dense, Input, Dropout, Embedding,SimpleRNN,Bidirectional,LSTM,Conv1D, GlobalMaxPooling1D,Activation,MaxPooling1D,GlobalAveragePooling1D
from keras.optimizers import RMSprop
from keras.utils import plot_model

#3
import tensorlayer as tl
import tensorflow as tf

#4
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
import ztools_draw as zdr
import ztools_tq as ztq
import zpd_talib as zta
#
import zai_keras as zks

#
#------------------------------------

#1
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    
rlog='/ailib/log_tmp'
if os.path.exists(rlog):tf.gfile.DeleteRecursively(rlog)

#2
print('\n#2,读取数据')
rss,fsgn,ksgn='/ailib/TDS/','TDS2_sz50','avg'
xlst=zsys.TDS_xlst9
zt.prx('xlst',xlst)
#
df_train,df_test,x_train,y_train,x_test, y_test=zdat.frd_TDS(rss,fsgn,ksgn,xlst)
print('\ndf_test.tail()')
print(df_test.tail())
print('\nx_train.shape,',x_train.shape)
print('\ntype(x_train),',type(x_train))

#3
print('\n#3,model建立神经网络模型')
num_in,num_out=len(xlst),1
print('\nnum_in,num_out:',num_in,num_out)
mx=zks.mlp020(num_in,num_out)
#
mx.summary()
plot_model(mx, to_file='tmp/mx002.png')


#4 模型训练
print('\n#4 模型训练 fit')
tbCallBack = keras.callbacks.TensorBoard(log_dir=rlog,write_graph=True, write_images=True)
tn0=arrow.now()
mx.fit(x_train, y_train, epochs=500, batch_size=512,callbacks=[tbCallBack])
tn=zt.timNSec('',tn0,True)
mx.save('tmp/mx002.dat')

#5 利用模型进行预测 predict
print('\n#5 模型预测 predict')
tn0=arrow.now()
y_pred = mx.predict(x_test)
tn=zt.timNSec('',tn0,True)
df_test['y_pred']=zdat.ds4x(y_pred,df_test.index,True)
df_test.to_csv('tmp/df_mlp020.csv',index=False)

