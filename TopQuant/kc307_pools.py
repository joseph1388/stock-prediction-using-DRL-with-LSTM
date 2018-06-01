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
import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
#
#
import zsys 
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
import ztools_draw as zdr
import ztools_tq as ztq
import zpd_talib as zta
#---------------------------


#1 set data 
xlst=['000001','000002']
clst=['600000','600016','600028','600029','600030','600036','600048','600050','600100','600104','600111','600340']
rss='/zDat/cn/day/'
rsx='/zDat/cn/xday/'
#----------
stkPools=zdat.pools_frd(rss,clst)
inxPools=zdat.pools_frd(rsx,xlst)
print('\n#1 type(stkPools)',type(stkPools))
print('type(inxPools)',type(inxPools))

#2 brow stkPools
print('\n#2 stkPools data')
xss=clst[3]
print('xss,',xss)
df=stkPools[xss]
print(df.tail())
#
#3,xed data avg10
avg10=zdat.pools_link2x(stkPools,clst,inxPools,xlst,'avg')
print('\n#3 avg10.head')
print(avg10.head())
print('\n avg10.tail')
print(avg10.tail())


#4,xed data avg20
avg10=avg10.dropna()
#avg10=avg10.tail(300)
a20=avg10.rebase()
a20=a20.round(2)

print('\n#4 avg20')
print('\n avg20.head')
print(a20.head())
print('\n avg20.tail')
print(a20.tail())

#plot
a20.plot()

