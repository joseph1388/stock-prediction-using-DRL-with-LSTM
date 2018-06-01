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
import ztools as zt
import ztools_datadown as zddown
import ztools_draw as zdr

#----------

#1 设置数据目录
#rss=zsys.rdatCN
rss='tmp/'
print('rss:',rss)



#2 设置股票代码，下载数据
code='603315'
df,fss=zddown.down_stk010(rss,code,'D')
df=df.sort_values(['date'],ascending=True);
print('\nfss,',fss)
print('\ndf')
print(df.tail())

#3 绘制K线图
print('\ndf2x.tail()')
df.index=df['date']
df2=df.tail(60)
hdr,fpic='k线图·日线数据-'+code,'tmp/tmp_.html'
print('\nfpic,',fpic)
print('\ndf2')
print(df2.tail())
zdr.drDF_cdl(df2,ftg=fpic,m_title=hdr)
