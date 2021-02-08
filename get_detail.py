import requests
import json
import time
from ip_pool import *
from cookie_pool import *
import pymongo
import os
import multiprocessing
from split_little import * 

def run_spider(i):
    # 从json文件中获取uid
    connection = pymongo.MongoClient('127.0.0.1', 27017)
    tdb = connection.fans_info
    post= tdb.fans2
    json_file="fans_id"+str(i)+".json"    
    headers={
            'Cookie':None,
            'Host':'m.weibo.cn',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'  
    }
    fans_profile_detail_url='https://m.weibo.cn/api/container/getIndex/'
    with open(json_file,'r',encoding='utf-8') as data:
        fans_dict=json.load(data)#将json对象变为了一个字典
        for key in fans_dict.keys():
            def get_fid(uid):
                cookie=get_random_cookie()
                headers['Cookie']=cookie
                proxy=get_random_proxy()
                fans_profile_url='https://m.weibo.cn/u/'+str(uid)
                res=requests.get(fans_profile_url,headers=headers,proxies=proxy)
                pid_raw=res.headers['Set-Cookie']
                index=pid_raw.rfind('fid%3D')
                pid=pid_raw[index+6:index+22]
                return pid
            uid=int(key)
            fid=get_fid(uid)

            def get_containerid(fid):
                cookie=get_random_cookie()
                headers['Cookie']=cookie
                proxy=get_random_proxy()
                payload={
                    'containerid':fid,
                    'type':'uid',
                    'value':uid
                }
                res=requests.get(fans_profile_detail_url,headers=headers,params=payload,proxies=proxy)
                con=json.loads(res.content)
                containerid=con['data']['tabsInfo']['tabs'][0]['containerid']
                return containerid
            
            containerid=get_containerid(fid)
            def get_fans_detail(containerid): 
                cookie=get_random_cookie()
                headers['Cookie']=cookie
                proxy=get_random_proxy()
                payload_detail={
                    'containerid':str(containerid)+'_-_INFO',
                    'title':'基本资料',
                    'lfid':containerid     
                }
                res=requests.get(fans_profile_detail_url,headers=headers,params=payload_detail,proxies=proxy)
                con=json.loads(res.content)
                fans_info={}
                try:
                    l0=len(con['data']['cards'][0]['card_group'])
                    for i in range(1,l0):
                        try:
                            fans_info[con['data']['cards'][0]['card_group'][i]['item_name']]=con['data']['cards'][0]['card_group'][i]['item_content']
                        except:
                            continue
                    l1=len(con['data']['cards'][1]['card_group'])
                    for i in range(1,l1):
                        try:
                            fans_info[con['data']['cards'][1]['card_group'][i]['item_name']]=con['data']['cards'][1]['card_group'][i]['item_content']
                        except:
                            continue

                    post.insert(fans_info)
                    print("进程:",os.getpid(),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"已将",uid,"粉丝信息存入mongo")

                except:
                    pass
    
                sleep_time=3*(random.random())
                while(sleep_time<2):
                    sleep_time=3*(random.random())
                time.sleep(sleep_time) #随机休眠2-3秒
            # print(i)
            get_fans_detail(containerid)
            # get_fans_detail(get_containerid(get_fid(uid)))
    
if __name__ == "__main__":
    # n为要开启的进程数目(推荐少开点)
    n=5
    # 拆分大文件n份
    split_little(n+1)

    for i in range(1,n+1):
        p=multiprocessing.Process(target=run_spider, args=(i,))
        p.start()
    # p.join()
   
        
#被逼无奈ip池和cookie池子都先抓下来放在本地
#写嵌套函数也非我本意,但不这样进程内部参数传不进去 

# 2078130765
# 1005052078130765
# 2302832078130765

# 经过抓包分析,需要先访问http://m.weibo.cn/u/+str(uid),在response.headers中找到containerid,再通过api携带参数访问主页,在这个返回的json里面提取出详细信息的containerid
# 再构造参数访问具体的详细信息页面,提取出想要的信息   
# 以下又是新的可爬取url
# https://m.weibo.cn/profile/3054324355
# https://m.weibo.cn/p/index?containerid=231051_-_fans_-_3054324355


# python语法,变量作用域LEGB



