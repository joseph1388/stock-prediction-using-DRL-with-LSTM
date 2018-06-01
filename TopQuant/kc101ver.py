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

import tensorflow as tf
import tensorlayer as tl
import keras as ks
import nltk

import pandas as pd
import tushare as ts
import matplotlib as mpl
import plotly
import arrow

#import tflearn
tflearn = tf.contrib.learn
#-----------------
#1
print('\n#1 tensorflow.ver:',tf.__version__)

#2
print('\n#2 tensorlayer.ver:',tl.__version__)

#3
print('\n#3 keras.ver:',ks.__version__)

#4
print('\n#4 nltk.ver:',nltk.__version__)


#5
print('\n#5 pandas.ver:',pd.__version__)

#6
print('\n#6 tushare.ver:',ts.__version__)

#7
print('\n#7 matplotlib.ver:',mpl.__version__)

#8
print('\n#8 plotly.ver:',plotly.__version__)


#9
print('\n#9 arrow.ver:',arrow.__version__)


#10
print('\n#10 tflearn.ver:')
