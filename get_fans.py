# https://m.weibo.cn/p/index?containerid=231051_-_fans_-_3982954755 你电粉丝主页
# https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_3982954755&since_id=2
import requests
import json
import time
from ip_pool import *
from cookie_pool import *

def clean_json():
    fileObj=open('fans_id.json','w',encoding='utf-8')
    fileObj.seek(0)
    fileObj.truncate()   #清空文件
    fileObj.close() 

def get_fans_id(since_id):
    # proxy=get_random_proxy(proxy_pool)
    # cookie=get_random_cookie(cookie_pool)
    # headers['Cookie']=cookie
    payload['since_id']=since_id
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"正在爬取第",page_num,"页粉丝信息")
    # print("using cookie:",cookie[-24:],"    using proxy:",proxy['proxy'])
    # res=requests.get(fans_url,params=payload,headers=headers,proxies=proxy)
    res=requests.get(fans_url,params=payload,headers=headers)
    con=json.loads(res.content)
    l=len(con['data']['cards'][0]['card_group'])
    for i in range(0,l):
        id=con['data']['cards'][0]['card_group'][i]['user']['id']
        fans_id[id]=con['data']['cards'][0]['card_group'][i]['user']['screen_name']

    jsObj=json.dumps(fans_id, ensure_ascii = False)
    fileObj=open('fans_id.json','w',encoding='utf-8')
    fileObj.write(jsObj)
    fileObj.close() 

if __name__ == "__main__":
    time_start=time.time()
    clean_json()
    # proxy_pool=get_proxy_pool()
    # cookie_pool=get_cookie_pool()
    time_end=time.time()

    fans_url='https://m.weibo.cn/api/container/getIndex/'
    # 以下containerid也可以从response的headers中获得
    payload={
        'containerid':'231051_-_fans_-_3982954755',
        'since_id':None
    }
    headers={
        'Cookie':'XSRF-TOKEN=03fa6c; WEIBOCN_FROM=1110006030; MLOGIN=0; loginScene=102003; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; SUB=_2A25NJJ5VDeRhGeNL6FMU9yfNzzuIHXVu5iIdrDV6PUJbkdAfLUKtkW1NSQKv0k_ZHhcDwsEtnBV_bLiTm4WnIM6i',
        'Host':'m.weibo.cn',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    
    fans_id={}
    for page_num in range(0,200):
        since_id = 1+20*page_num
        get_fans_id(since_id)
    time_end=time.time()
    print('all time cost',time_end-time_start,'s')
    
    