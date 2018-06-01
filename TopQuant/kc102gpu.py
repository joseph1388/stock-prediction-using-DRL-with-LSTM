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

#-----------------
#1
print('\n#1')
cfig=tf.ConfigProto(log_device_placement=True)
hello = tf.constant('Hello, TensorFlow!')
print('tf.__version__:',tf.__version__)

#2
print('\n#2')
sess = tf.Session(config=cfig)
dss=sess.run(hello)
print(dss)

#
#3
print('\n#3')
a = tf.constant(11)
b = tf.constant(22)
ds2=sess.run(a + b)
print(ds2)

#
#4
print('\n#4')
a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
c = tf.matmul(a, b)
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
ds3=sess.run(c)
print(ds3)

#5
print('\n#5')
sess.close()
