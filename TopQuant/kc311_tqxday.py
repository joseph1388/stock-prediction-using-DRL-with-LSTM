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
codLst=[]
inxLst=['000001']
rs0=zsys.rdatCN0  #'/zDat/cn/'
print('\n#1,set data,init,',rs0)
qx=ztq.tq_init(rs0,codLst,inxLst)
#



#3
xcod=qx.wrkInxCod
print('\n#3,qx.wrkInx')
print('\nqx.wrkInxCod,',qx.wrkInxCod)
print('\nqx.wrkInxFinfo,',qx.wrkInxInfo)
print('\nqx.wrkInxDat.tail')
print(qx.wrkInxDat.tail())

#
#4--plot
print('\n#4,plot-->tmp/tmp_.html')
hdr,fss='k线图-指数:'+xcod,'tmp/tmp_.html'
df2=qx.wrkInxDat.tail(100)
zdr.drDF_cdl(df2,ftg=fss,m_title=hdr)

