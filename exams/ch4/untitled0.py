# -*- coding: utf-8 -*-
"""
Created on Mon May 28 21:52:22 2018

@author: joseph
"""

#!/usr/bin/env python  
# _*_ coding: utf-8 _*_  
  
import tensorflow as tf  
import numpy as np  
  
input1 = tf.placeholder(tf.float32)  
input2 = tf.placeholder(tf.float32)  
  
output = tf.multiply(input1, input2)  
  
with tf.Session() as sess:  
    print (sess.run(output, feed_dict = {input1:[3.], input2: [4.]})  )
    
   
a = tf.constant([[1,2,3],[3,4,5]]) # shape (2,3)
b = tf.constant([[7,8,9],[10,11,12]]) # shape (2,3)
c = tf.stack([a,b],axis=0)
d = tf.unstack(c,axis=0)
e = tf.unstack(c,axis=1)
ab = tf.stack([a,b], axis=2) # shape (2,2,3)
print ('a shape =',a.get_shape())
print ('b shape =',b.get_shape())
print ('c shape =',c.get_shape())
print ('ab shape =',ab.get_shape())
with tf.Session() as sess:
    print('c= ',sess.run(c))
    print('d= ',sess.run(d))
    print('e= ',sess.run(e))
    print('ab = ',sess.run(ab))