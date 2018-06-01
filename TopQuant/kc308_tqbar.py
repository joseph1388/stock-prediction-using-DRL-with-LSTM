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

#  TopQuant
import zsys 
import zpd_talib as zta
import ztools as zt
import ztools_tq as ztq
import ztools_data as zdat


#----------

#1 set data,init
inxLst=['000001','000002']
codLst=['600000','600016','600028','600029','600030','600036','600048','600050','600100','600104','600111','600340']
rs0=zsys.rdatCN0  #'/zDat/cn/'
print('\n#1,set data,init,',rs0)
qx=ztq.tq_init(rs0,codLst,inxLst)


#2
print('\n#2,qt.prVars(qx)')
ztq.tq_prVars(qx)

