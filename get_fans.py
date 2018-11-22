# https://m.weibo.cn/p/index?containerid=231051_-_fans_-_3982954755
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

def get_fans_id():
    proxy=get_random_proxy(proxy_pool)
    cookie=get_random_cookie(cookie_pool)
    headers['Cookie']=cookie
    payload['since_id']=page_num
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"正在爬取第",page_num,"页粉丝信息")
    print("using cookie:",cookie[-24:],"    using proxy:",proxy['proxy'])
    res=requests.get(fans_url,params=payload,headers=headers,proxies=proxy)
    con=json.loads(res.content)
    if(page_num==1):
        x=3
    else:
        x=0
    l=len(con['data']['cards'][x]['card_group'])
    for i in range(0,l):
        id=con['data']['cards'][x]['card_group'][i]['user']['id']
        fans_id[id]=con['data']['cards'][x]['card_group'][i]['user']['screen_name']

    jsObj=json.dumps(fans_id, ensure_ascii = False)
    fileObj=open('fans_id.json','w',encoding='utf-8')
    fileObj.write(jsObj)
    fileObj.close() 

if __name__ == "__main__":
    time_start=time.time()
    clean_json()
    proxy_pool=get_proxy_pool()
    cookie_pool=get_cookie_pool()
    time_end=time.time()
    print('reflash cookie_pool time cost',time_end-time_start,'s')

    fans_url='https://m.weibo.cn/api/container/getIndex/'
    # 以下containerid也可以从response的headers中获得
    payload={
        'containerid':'231051_-_fans_-_3982954755',
        'since_id':None
    }
    headers={
        'Cookie':'_T_WM=c266497ccd9f46eb7e0024ee107e4999; SUB=_2A25249siDeRhGeBK6lAW9SrKzDuIHXVSL-VqrDV6PUJbkdBeLRSikW1NR_acECxNrw3nYjVJvkhIkqkYZpyTDfws; SUHB=08J7w3zcIyb1yC; SCF=AhTC4fQKIQNff_LJvKN5pccJM4WjxlfsVmIvuJfqENrBfvO5UL9m3Mb06UcwIqnZb3AbBWZ5pOYRrVBkD_DjduQ.; MLOGIN=1; M_WEIBOCN_PARAMS=featurecode%3D10000326%26luicode%3D10000011%26lfid%3D231051_-_fans_-_5042403328%26fid%3D231051_-_fans_-_5042403328%26uicode%3D10000011; WEIBOCN_FROM=1110003030',
        'Host':'m.weibo.cn',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    
    fans_id={}
    for page_num in range(1,2000):
        get_fans_id()
    time_end=time.time()
    print('all time cost',time_end-time_start,'s')
    
    