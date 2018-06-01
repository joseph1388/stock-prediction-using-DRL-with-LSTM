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
import ztools_datadown as zddown

#----------

#下载股票日线数据文件，
#1
#rs0=zsys.rdatMin0+'M05/'
rs0=zsys.rdatMin0
print('rs0:',rs0)

#
xtyp='5'
xss=xtyp
if len(xtyp)==1:xss='0'+xss
rss=rs0+'M'+xss+'/'
print('rss#1:',rss)
#
rss='tmp/'
print('rss#2:',rss)
#
#2，设置股票代码文件 ，批量下载数据
#finx='inx\\stk_code.csv';
finx='data/stk_pool.csv';
zddown.down_stk_all(rss,finx,xtyp)

