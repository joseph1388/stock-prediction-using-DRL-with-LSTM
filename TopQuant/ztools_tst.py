#coding=utf-8
# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 


网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
    
TopQuant.vip ToolBox 2016
Top极宽·量化开源工具箱 系列软件 
by Top极宽·量化开源团队 2016.12.25 首发
  
文件名:ztools_tst.py
默认缩写：import ztools_tst as ztst
简介：Top极宽常用工具函数集
'''

import os,sys,io,re
import random,arrow,bs4
import numpy as np
import numexpr as ne
import pandas as pd
import tushare as ts

import requests
from functools import wraps
#
import cpuinfo as cpu
import psutil as psu
#
import matplotlib as mpl
import matplotlib.colors
from matplotlib import cm

#
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_web as zweb

#

#-----------------------
'''
var&const
#

fun.tst
#
xobj.xxx
lst.xxx
file.xxx
f.lst.xxx

'''

#-----------------------
#----------var&const
zt_fun_tst_time_nloop=5
                
#----------fun.test


def fun_tim01(function):
    @wraps(function)
    def fun_tim(*args, **kwargs):
        t0 = arrow.now()
        result = function(*args, **kwargs)
        tn=zt.timNSec(arrow.now(),t0)
        print ('tn,{0:.3f}s,fun:{1}'.format(tn,function.__name__))
        return result
    return fun_tim

def fun_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        xt0=999999;xt9=0;xtn=0;xtsum=0;
        for xc in range(zt_fun_tst_time_nloop):
            t0 = arrow.now()
            tfn = function(*args, **kwargs)
            t1 = arrow.now()
            xtn=t1-t0
            xt0=min(xt0,xtn);xt9=max(xt9,xtn)
            xtsum=xtsum+xtn
            #print ("  %d # ,t:%.4f s,t.min:%.4f s,  t.max:%.4f s, t.sum:%.4f s " % (xc,xtn,xt0,xt9,xtsum))
            
        #
        xt5=xtsum/zt.zt_fun_tst_time_nloop;
        #print('')
        #print('xt5,',xt5,zt_fun_tst_time_nloop)
        #print ("  %d # trd, %.4f s" % (args[1],t1-t0))
        print ("  %d # trd, t:%.6f s, t0:%.6f s, t9:%.6f s" % (args[1],xt5,xt0,xt9))
        
        
        #print('var',args[1])
        return xt5,xt0,xt9
        
    return function_timer

def fun_tim050(func,dat,css):
    xt0=999999;xt9=0;xtn=0;xtsum=0;
    for xc in range(zt_fun_tst_time_nloop):
        t0 = arrow.now()
        func(dat)
        t1 = arrow.now()
        xtn=t1-t0
        xt0=min(xt0,xtn);xt9=max(xt9,xtn)
        xtsum=xtsum+xtn
    #
    xt5=xtsum/zt_fun_tst_time_nloop;
    print ("%s,%s, t:%.6f s, t0:%.6f s, t9:%.6f s，nloop:%d" % (css,func.__name__,xt5,xt0,xt9,zt_fun_tst_time_nloop))
    #print('tn:%.6f,%s'%(t1-t0,func.__name__))

    
def fun_tim010(func,dat):
    
    t0 = arrow.now()
    func(dat)
    t1 = arrow.now()
    print('tn:%.6f,%s'%(t1-t0,func.__name__))
    

def fun_tim010call():
    arr = np.arange(9999999).reshape(3333333,3)
    dnum=50000000;d_np=np.arange(dnum)
    #
    #zz_tst010(abs001,d_np,'py tn:')
    #zz_tst010(abs001_nb,d_np,'nb tn:')
    #zz_tst010(abs001_ex,d_np,'ex tn:')
    #
    #fun_tim010(sum2d,arr)
    #fun_tim010(sum2d_nb,arr)
    
    
