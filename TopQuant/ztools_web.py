#coding=utf-8
# -*- coding: utf-8 -*- 
'''
Top极宽量化(原zw量化)，Python量化第一品牌 

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化1群，124134140
      Top极宽量化2群，650924099
      Top极宽量化3群，450853713
  
    
TopQuant.vip ToolBox 2016
Top极宽·量化开源工具箱 系列软件 
by Top极宽·量化开源团队 2016.12.25 首发
  
文件名:ztools_web.py
默认缩写：import ztools_web as zweb
简介：Top极宽web网络与htm网页常用工具函数集
'''

import os,sys,io,re
import arrow,bs4,random
import pandas as pd
import tushare as ts
#
import requests
import bs4
from bs4 import BeautifulSoup 
from robobrowser import RoboBrowser 
from concurrent import futures
from concurrent.futures import ProcessPoolExecutor, as_completed
#

import zsys
import ztools as zt
import ztools_str as zstr
import ztools_data as zdat
#
#-----------------------
'''
xxx.var&const
misc
#
web_get_xxx    
web_get_xxx.site...
#
#--web_dz.xxx   ,discuz
#----zdz.zwx.xxx   zdz.zwx-->zdzx
#---bs4.xxx
'''
#-----------------------

#------------web.var&const
zt_headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
zt_xagent='Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

                       

#-----------------------


    
#---web_get_xxx    
    
def web_get001(url):
    try:
        rx= requests.get(url,headers=zt_headers)  #获得网页,headers
    except:
        rx=None
        return None
    finally:
        return rx
    #
    return rx    
   

def web_get001txt(url,ucod='gb18030',ftg='',fcod='gbk'):
    htm,rx='',web_get001(url)
    if rx!=None:
        xcod=rx.apparent_encoding;#print(xcod,uss)
        rx.encoding =xcod  #gb-18030
        #dss=rx.text
        htm=rx.text;#print(htm)
        if xcod.upper()=='UTF-8':
            #print('@@u8a');#print(htm)
            htm=htm.replace('&nbsp;',' ')
            css = htm.encode("UTF-8",'ignore').decode("UTF-8",'ignore')
            css=css.replace(u'\xfffd ', u' ')
            css=css.replace(u'\xa0 ', u' ')
            htm = css.encode("GBK",'ignore').decode("GBK",'ignore')
        #
        if ftg!='':zt.f_add(ftg,htm,True,cod=fcod)
    #
    return htm
    
    
def web_get001txtFg(uss,fss):
    fsiz=zt.f_size(fss)
    if zsys.web_get001txtFg or(fsiz<1000):
        #print(zsys.sgnSP8,fss,fsiz)
        #uss=xtfb.us0_extOuzhi+xtfb.kgid+'.shtml';#print(uss)
        htm=web_get001txt(uss,ftg=fss,fcod='GB18030');#print(fss)
    else:
        htm=zt.f_rd(fss,cod='GB18030')    
    #
    return htm
    
    
def web_getXLnks(url,ckn=10,kget=None,kflt=None,uget=None,uflt=None,ucod='gbk'):
    #rx= requests.get(url,headers=zt_headers)  #获得网页,headers
    #print(url)
    df=pd.DataFrame(columns=['hdr','url'])
    rx=web_get001(url)
    if rx==None:return df
    #
    #rx.encoding =ucod #gb-18030
    bs=BeautifulSoup(rx.text,'html5lib') # 'lxml'
    #bs=bs0.prettify('utf-8')
    xlnks=bs.find_all('a');#print(xlnks)
    
    ds=pd.Series(['',''],index=['hdr','url'])
    #print('\ncss,xss:',klnk,kflt)
    for lnk in xlnks:
        css,uss=lnk.text,lnk.get('href')
        #print('cs0,',css,uss)
        #
        if uflt!=None and uss!=None and zstr.str_xor(uss,uflt):uss=None
        if uget!=None and uss!=None and (not zstr.str_xor(uss,uget)):uss=None
        #
        if kflt!=None and uss!=None and zstr.str_xor(css,kflt):uss=None
        if kget!=None and uss!=None and (not zstr.str_xor(css,kget)):uss=None
        #print('cs2,',css,uss)
        #
        if uss==None:css=''
        css=zstr.str_fltHtmHdr(css)
        if len(css)>ckn:
            css=css.replace(',','，')
            #print('css,xss:',css,uss)
            ds['hdr'],ds['url']=css,uss
            df=df.append(ds.T,ignore_index=True)
    #
    #print(df)    
    return df    
    


def web_getXTxt001div(bs,claSgn):
    x10,tss=bs.find_all('div'),''
    for x in x10: 
        #print('@x',x)
        if x!=None:
            x2=x.find('div',class_=claSgn)
        else:x2=None
        #
        if x2!=None:
            css=x2.text
            if tss.find(css)==-1:
                css=zstr.str_fltHtm(css)
                tss=''.join([tss,'\n',css])
                #print("@::",css,'\ncsn,',len(css))
                #print("@::",x2)
    #
    #tss=tss+'\n'+claSgn
    if len(tss)<200:tss=''
    return tss
    
    
def web_getXTxt001k(bs):
    x10,tss=bs.find_all('p'),''
    if x10==[]:x10=bs.find_all('div')
    for x in x10: 
        if x!=None:
            css=x.text
            if tss.find(css)==-1:
                css=zstr.str_fltHtm(css)
                if len(css)>10:
                    tss=''.join([tss,'\n',css])
                    #print(css);print('csn',len(css))
    #
    #tss=tss+'\np'
    if len(tss)<200:tss=''
    return tss
    
def web_getXTxt010x9(uss,ucod='gb18030'):
    htm=web_get001txt(uss)
    if htm=='':return ''
    #
    
    bs=BeautifulSoup(htm,'html5lib') # 'lxml'
    if bs.title==None:return ''
    #
    if uss.find('.zhihu.com')>0:
        tss=web_getXTxt001div(bs,'zm-editable-content')
    else:
        tss=web_getXTxt001k(bs);
    #    
    return tss     
  
    
def web_getXTxt100(df,rs0,txtn0=200):
    for i, row in df.iterrows():
        uss,hdr,txt=row['url'],row['hdr'],''
        hdr = re.sub('[\\\/:*?"<>|]','-',hdr)          
        if len(uss)>20:txt=web_getXTxt010x9(uss);#print('h2,',chdr)
        #
        if len(txt)>txtn0:
            
            rss=rs0
            if not os.path.exists(rss):os.mkdir(rss)
            #
            fss=rss+hdr+'.txt';print('    ',fss)
            css=hdr+'\n'+uss+'\n\n'+txt
            #print(css,'\n',fss)
            zt.f_add(fss,css,True)

#--- web_get_xxx.site...
            
def web_get_bdnews010(kstr,pn=1):
    url_bdnews0='http://news.baidu.com/ns?cl=2&ct=0&rn=50&ie=gbk&word={0}&pn={1}'  #pn=50x
    #
    df9=pd.DataFrame(columns=['hdr','url'])
    for xc in range(0,pn):
        uss=url_bdnews0.format(kstr,xc*50);print(uss)
        df=web_getXLnks(uss);
        df9=df9.append(df,ignore_index=True)
    #
    df9=df9.drop_duplicates(['hdr'])
    return df9
    
def web_get_cnblog010(kstr,timSgn='OneWeek',npg=2):
    us0='http://zzk.cnblogs.com/s/blogpost?DateTimeRange='+timSgn+'&Keywords={0}&pageindex={1}'
    df9=pd.DataFrame(columns=['hdr','url'])
    for xc in range(0,npg):
        uss=us0.format(kstr,xc);print(uss)
        df=web_getXLnks(uss);
        df9=df9.append(df,ignore_index=True)
    #
    df9=df9.drop_duplicates(['hdr'])
    return df9
    
   
def web_get_zhihu010(kstr):
    #1d=day;1w=week
    uss='https://www.zhihu.com/search?type=content&range=1w&q={0}'.format(kstr);
    #print( uss)
    df=web_getXLnks(uss,uget=['/question'],uflt=['/answer']);#print(df)
    #https://www.zhihu.com/question/21063634
    if len(df['hdr'])>0:
        df['url']='https://www.zhihu.com'+df['url']
        print(df)
        
    
    return df
#-----------------------

   
#--web_dz.xxx   
    
def zdz_post010(uid,unam,upas,chdr,ctxt,uhost='http://ziwang.com/'):
    brow = RoboBrowser(history=True,cache=True)
    uexit=uhost+'member.php?action=logout'
    brow.open(uexit);zt.wait(1)
    #
    ulog=uhost+'forum.php' #,'58'  #灌水乐园 
    brow.open(ulog);zt.wait(2);#print('ulog,',ulog)   
    xact="member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes"
    xlog=brow.get_form(action=xact);#print('xlog',xlog)
    if xlog==None:return False
    print('@xlog,',unam,upas)
    #
    xlog['username'].value=unam
    xlog['password'].value=upas
    brow.submit_form(xlog)
    #
    #       http://ziwang.com/forum.php?mod=post&action=newthread&fid=67
    upost0='http://ziwang.com/forum.php?mod=post&action=newthread&fid='
    upost=upost0+uid;#print('@xpost, ',uid,upost);
    x=brow.open(upost);zt.wait(1)
    xact_post='forum.php?mod=post&action=newthread&fid='+uid+'&extra=&topicsubmit=yes'
    xpost=brow.get_form(action=xact_post)
    #print('@xpost, ',xpost)
    #
    xpost['subject'].value,xpost['message'].value=chdr,ctxt
    brow.submit_form(xpost)
    #print('@xpost, ',upost);
    #
    #re_brow,upost,chk_post
    return True
    

def zdz_getKHdrFlt9(df9,dfnew,rsk):
    #dfnew=dfnew.dropna_duplicates(['hdr'])
    dfnew=dfnew.dropna()
    for i, row in dfnew.iterrows():
        hdr=row['hdr'];#print('\n',hdr)
        if hdr!=None:
            xfg=zdat.df_strFind01(df9['hdr'],hdr);#print('\ndf9,',xfg,hdr)
            if not xfg:
                fss=''.join([rsk,hdr,'.txt'])      
                xfg=os.path.exists(fss);#print(xfg,fss)
            if not xfg:
                fss=''.join([rsk,'zz_',hdr,'.txt']);
                xfg=os.path.exists(fss);#print(xfg,fss)
            #
            #print(xfg,i)
            if xfg:
                dfnew.iloc[i-1]['hdr'],dfnew.iloc[i-1]['url']=None,None
    #
    dfnew=dfnew.dropna()#_duplicates(['hdr'])
    return dfnew
        
def zdz_getKHdr050(kstr,rsk,df9_hdr):
    df_hdr=web_get_bdnews010(kstr,1)
    df=web_get_cnblog010(kstr);df_hdr=df_hdr.append(df,ignore_index=True)
    df=web_get_zhihu010(kstr);df_hdr=df_hdr.append(df,ignore_index=True)
    #
    #df_hdr.to_csv('tmp/new010_'+kstr+'a1.csv',index=False)
    df_hdr=df_hdr.drop_duplicates(['hdr'])
    df_hdr=zdz_getKHdrFlt9(df9_hdr,df_hdr,rsk)
    #df_hdr.to_csv('tmp/new010_'+kstr+'ax.csv',index=False)
    #
    return df_hdr

#----zdz.zwx.xxx   
def zwx_finx2urls(pn9=9,finx='dat/zw_bbs30k.csv',us0='http://ziwang.com/'):
    df_inx=pd.read_csv(finx,index_col=False,encoding='gbk')    #print(df_inx.tail())
    urls=[]
    for i, row in df_inx.iterrows():
        fid=row['uid']
        us2=''.join([us0,'forum.php?mod=forumdisplay&fid=',str(fid)])
        for xc in range(0,pn9):
            uss=''.join([us2,'&page=',str(xc)]);#print(uss);
            urls.append(uss)
    #
    return urls
    
def zwx_getHdr001(uss):
    #print('    x1,',uss)
    df=web_getXLnks(uss,10);#print(df.tail())
    print('    x9,',uss)
    return df

    

def zwx_getHdr500(pn9=9,ftg='tmp/dz100hdr.csv',finx='dat/zw_bbs30k.csv',us0='http://ziwang.com/'):
    df_inx=pd.read_csv(finx,index_col=False,encoding='gbk')    #print(df_inx.tail())
    df9=pd.DataFrame(columns=['hdr','url'])
    for i, row in df_inx.iterrows():
        fid,hdr=row['uid'],row['hdr'];#print(fid,hdr)
        #http://ziwang.com/forum.php?mod=forumdisplay&fid=48&page=6
        us2=''.join([us0,'forum.php?mod=forumdisplay&fid=',str(fid)])
        for xc in range(0,pn9):
            uss=''.join([us2,'&page=',str(xc)]);#print(uss);
            df=web_getXLnks(uss,10);#print(df.tail())
            if len(df['hdr'])>0:    
                df2=df[df['url'].str.contains('viewthread',na=False)];
                df9=df9.append(df2)
                print(fid,hdr,'xn9,',len(df9['hdr']),uss)
    #
    df9=zdat.df_fltHdr(df9)
    df9.to_csv(ftg,index=False)
    print('xn9',len(df9['hdr']),'\n')
    #
    return df9    

  

def zwx_getHdr500pool(nsub=5,pn9=9,ftg='tmp/dz100hdr.csv'):
    df9=pd.DataFrame(columns=['hdr','url'])
    urls=zwx_finx2urls(pn9)
    #
    #pool = ProcessPoolExecutor(max_workers = nsub)  #as ex
    pool=ThreadPoolExecutor(max_workers = nsub)
    xsubs = [pool.submit(zwx_getHdr001,uss) for uss in urls]
    #
    for xsub in as_completed(xsubs):
        df=xsub.result(timeout=20);
        if len(df['hdr'])>0:
            df2=df[df['url'].str.contains('viewthread',na=False)];
            df9=df9.append(df2)
            #print(df9.tail());
            #print('xn9,',len(df9['hdr']),'#nsub,',str(nsub))
    #
    df9=df_fltHdr(df9)
    #print(df9)
    #df9.to_csv(ftg,index=False,encoding='gbk')
    df9.to_csv(ftg,index=False,encoding='gbk')
    print('xn9',len(df9['hdr']),'\n')
    #
    return df9
    
def zwx_post010(fsr0,rsk,uid,unam,upas,df9_hdr):
    fss=rsk+fsr0
    
    chdr,ctxt=f_rdXHdr(fss,cod='gbk');
    chdr2,ctxt2=chdr.encode("gbk"),ctxt.encode('gbk')
    fs2=rsk+'zz_'+fsr0;
    if os.path.exists(fs2):os.remove(fss);
    #
    #print('chdr',chdr);print('chdr2',chdr2)
    ntxt,fgRename,fgFindHdr=len(ctxt),False,df_strFind01(df9_hdr['hdr'],chdr)
    #print('ntxt',ntxt,fgRename,fgFindHdr,chdr)
    if (ntxt<200)or(fgFindHdr):
        fgRename=True
    else:
        xfg=zdz_post010(uid,unam,upas,chdr2,ctxt2)
        if xfg:fgRename=True
    #
    if fgRename:os.rename(fss,fs2)
        #print('xchdr',chdr)
    
def zwx_post100(ulst,rsk,uid,df9_hdr):
    flst=zt.lst4dir(rsk);#flst=flst[:5]#zt.lstPr(flst)
    flst=zt.lst_keyFltStr(flst,'zz_')
    fn9,nusr=len(flst),len(ulst['nam'])-1
    ns9='/'+str(fn9);print('fn9,',fn9)
    #
    #flst=flst[:1];#print(flst)
    for i, fn0 in enumerate(flst):
        print(i,ns9,'#',rsk,fn0)
        xc=random.randint(0,nusr);#xc=10
        unam,upas=ulst.nam[xc],ulst.pas[xc]
        #    
        zwx_post010(fn0,rsk,uid,unam,upas,df9_hdr)
    #

                
def zwx_main500(xc0,xnk=1,fgGet=1,rs0='txt/',fhdr9='tmp/dz100hdr.csv',fkey='dat/zw_bbs30_xkey.csv',fusr='dat/zw_usr2017m1k.dat'):
    df=pd.read_csv(fkey,index_col=False,encoding='gbk')
    df9_hdr=pd.read_csv(fhdr9,index_col=False,encoding='gbk')
    ulst=pd.read_csv(fusr,index_col=False)
    xn9=len(df['xkey']);xn=min(xn9,xc0+xnk)  
    #print('x,',xn,xn9,xc0,xc0+xnk)      
    #print(df.head());print(df9_hdr.head())
    for xc in range(xc0,xn):
        ds=df.iloc[xc]
        kstr,uid=ds['xkey'],str(ds['uid'])
        rsk=''.join([rs0,kstr,'/']);
        #print(xc,'kstr,uid,',kstr,uid)
        #
        if fgGet==1:
            df_new=zdz_getKHdr050(kstr,rsk,df9_hdr)    
            print(df_new.head())
            df_new.to_csv('tmp/new010_'+kstr+'.csv',index=False,encoding='gbk')
            web_getXTxt100(df_new,rsk)    
        #
        #  post
        zwx_post100(ulst,rsk,uid,df9_hdr)


    #    
#------bs4.xxx
def bs_get_ktag(tag):
    #return tag.has_attr('isend')
    #print('k',fb_get_ktag_kstr)
    return tag.has_attr(zsys.bs_get_ktag_kstr)
    