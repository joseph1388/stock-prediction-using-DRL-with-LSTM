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

import os,arrow  
import numpy as np
import pandas as pd
import tushare as ts

#  TopQuant
import zsys 
import ztools as zt
import ztools_datadown as zddown
import ztools_draw as zdr

#----------

#1 设置数据文件目录，参数

rss=zsys.rdatReal
print('rss#1:',rss)
rss='tmp/'
zt.f_dirDel(rss)  
print('rss#2:',rss)
#      
xtyp='5'
tim=arrow.now().format('YYYY-MM-DD')
print('t',tim,xtyp)
#
#2 下载股票实时数据文件
xcod='603316'
df=zddown.down_min_real010(rss,xcod,xtyp=xtyp,fgIndex=False)
print('\nxcod:',xcod)
print(df.tail())
hdr,fss='k线图-'+xcod,'tmp/tmp_'+xcod+'.html'
df.index=df['date']
zdr.drDF_cdl(df,ftg=fss,m_title=hdr)

#
#3 下载指数实时数据文件
xcod='000001' #上证指数
df2=zddown.down_min_real010(rss,xcod,xtyp=xtyp,fgIndex=True)
print('\nxcod:',xcod)
print(df2.tail())
hdr,fss='k线图-'+xcod,'tmp/tmp_'+xcod+'.html'
df2.index=df2['date']
zdr.drDF_cdl(df2,ftg=fss,m_title=hdr)
