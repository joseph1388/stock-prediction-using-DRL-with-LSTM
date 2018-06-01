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

import os,ffn
import numpy as np
import pandas as pd
import tushare as ts
import plotly as py
import plotly.figure_factory  as pyff

#  TopQuant
import zsys 
import zpd_talib as zta
import ztools as zt
import ztools_tq as ztq
import ztools_draw as zdr
import ztools_data as zdat


#----------


#1 预处理
pd.set_option('display.width', 450)    
pyplt=py.offline.plot    
#---------------

#2 set data,init
codLst=['000001','000002']
inxLst=['000001','000002']
rs0=zsys.rdatCN0  #'/zDat/cn/'
print('\n#2,set data,init,',rs0)
qx=ztq.tq_init(rs0,codLst,inxLst)
#

#3
#3.A
print('\n#3.A,qx.wrkStk')
xcod=qx.wrkStkCod
print('\nqx.wrkStkCod,',qx.wrkStkCod)
print('\nqx.wrkStkInfo,',qx.wrkStkInfo)
#3.B
xcod=qx.wrkInxCod
print('\n#3.B,qx.wrkInx')
print('\nqx.wrkInxCod,',qx.wrkInxCod)
print('\nqx.wrkInxFinfo,',qx.wrkInxInfo)

#
#4--plot
print('\n#4,plot-->tmp/tmp_.html')


#4
print('\n#4 plot#1.')
df_inx=qx.wrkInxDat
df_stk=qx.wrkStkDat
nam_inx=qx.wrkInxInfo.ename.values[0]
nam_stk=qx.wrkStkInfo.ename.values[0]
print('\nnam_inx:',nam_inx)
print('nam_stk:',nam_stk)
#
df9=pd.DataFrame()
ksgn='close'
df9[nam_inx]=df_inx[ksgn]
df9[nam_stk]=df_stk[ksgn]
print('\ndf9.tail()')
print(df9.tail())
#
df9[nam_stk]=df9[nam_stk]*100
print('\ndf9.tail()*100')
print(df9.tail())
#df9[xinx2css]=xinx2Dat['close']
df9=df9.dropna()
df9.plot()

#
#5
print('\n#5 plot#2')
ksgn='avg'
zdat.pools_link2qx(qx,ksgn)
avg10=qx.wrkPriceDat
print('\navg10.head')
print(avg10.head())
print('\navg10.tail')
print(avg10.tail())


#4,xed data avg20
avg10=avg10.dropna()
#avg10=avg10.tail(300)
a20=avg10.rebase()
a20=a20.round(2)

print('\navg20')
print('\navg20.head')
print(a20.head())
print('\navg20.tail')
print(a20.tail())
#plot
a20.plot()


