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

import pandas as pd
import plotly as py
import plotly.figure_factory  as pyff
#from plotly.tools import FigureFactory as pyff


#
import zsys
import zpd_talib as zta
import ztools as zt
import ztools_str as zstr
import ztools_draw as zdr
import ztools_tq as ztq

#
#================================
#1 预处理
pd.set_option('display.width', 450)    
pyplt=py.offline.plot    
#---------------

#2
fss='data/002645_2016-09-01.csv'
df=pd.read_csv(fss,index_col=False)
df=df.sort_values('time')
print('\n#2,df.tail()')
print(df.tail())

#3
df1min=ztq.tick2x(df,ktim='1min')
print('\n#3 @1min\n',df1min.tail());
     
#4
df1T=ztq.tick2x(df,ktim='1T')
print('\n#4 @1T\n',df1T.tail());

          
#5
df1D=ztq.tick2x(df,ktim='1D')
print('\n#5 @1D\n',df1D.tail());
     
#6
df30s=ztq.tick2x(df,ktim='30S')
print('\n#6 @30S\n',df30s.tail());     

#7
df15min=ztq.tick2x(df,ktim='15min')
print('\n#7 @15min\n',df15min.tail());
     
#8
print('\n#8,plot-->tmp/tmp_.html')
hdr,fss='15分钟分时K线图','tmp/tmp_.html'
df2=df15min.tail(200)
zdr.drDF_cdl(df2,ftg=fss,m_title=hdr)

#9
print('\n#4,ok')
