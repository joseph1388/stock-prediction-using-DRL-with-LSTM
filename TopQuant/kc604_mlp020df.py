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
#1
import os,arrow
import pandas as pd
import numpy as np

#4
import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
import ztools_draw as zdr
import ztools_tq as ztq
import zpd_talib as zta
#


#
#------------------------------------

#1
print('\n#1,set.sys')
pd.set_option('display.width', 450)    
pd.set_option('display.float_format', zt.xfloat3)    

#2
print('\n#2,读取数据')
fss='data/df_mlp020.csv'
df=pd.read_csv(fss)
zt.prx('df',df.tail())
#

#3 
print('\n#3 整理数据')
df2=df[df.y_pred>0]
zt.prx('df2',df2.tail())
print('\ndf.num,',len(df.index))
print('\ndf2.num,',len(df2.index))

#4 
print('\n#4 acc准确度分析')
print('\nky0=10')
dacc,dfx,a10=ztq.ai_acc_xed2ext(df2.y,df2.y_pred,ky0=10,fgDebug=True)

print('\nky0=5')
dacc,dfx,a10=ztq.ai_acc_xed2ext(df2.y,df2.y_pred,ky0=5,fgDebug=True)

#5 
print('\n#5 图形分析')
df2[['y','y_pred']].plot()
#
df3=df2[df2.y<100]
df3[['y','y_pred']].plot()


