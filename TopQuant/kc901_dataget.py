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
#1 数据文件总目录
rs0=zsys.rdatCN0
print('\n#1 rs0:',rs0)

#2 指数索引文件,数据文件保存目录
finx,rss='inx\\inx_code.csv',rs0+'xday/'
print('\n#2,finx,',finx)
#下载大盘指数文件，
zddown.down_stk_inx(rss,finx);


#------------------------------
#3.1,下载股票分时数据文件
rsm=zsys.rdatMin0
print('\n#3,rsm:',rsm)
#
xtyp='5'
xss=xtyp
if len(xtyp)==1:xss='0'+xss
rss=rsm+'M'+xss+'/'
print('rss:',rss)
#
#finx='inx\\stk_code.csv';
finx='data\\bt-stk06.csv';
#codLst=['000001','002046','600663','000792','600029','000800']
print('\n#3.1 下载股票分时数据，finx,',finx)
zddown.down_stk_all(rss,finx,xtyp)


#3.2，下载指数分时数据文件，
print('\n#3.2 下载指数分时数据，finx,',finx)
#rs0=zsys.rdatMin0+'M05/'
rss=rs0+'XM'+xss+'/'
finx='inx\\inx_code.csv';
zddown.down_stk_all(rss,finx,xtyp,True)

#--------------
 
#4下载股票日线数据文件，
rss=rs0+'day/' 
print('\n#4,rss:',rss)

#
#finx='inx\\stk_code.csv';
finx='data\\bt-stk06.csv';
zddown.down_stk_all(rss,finx,'D')

