import requests
import re
import json
import time
import random
import os
from bs4 import BeautifulSoup
from ip_pool import get_random_proxy,get_proxy_pool
from cookie_pool import get_cookie_pool,get_random_cookie

def clean_json():
    fileObj=open('data1.json','w',encoding='utf-8')
    fileObj.seek(0)
    fileObj.truncate()   #清空文件
    fileObj.close() 

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

def prase_weibo(mid):
    detail_url='https://m.weibo.cn/detail/'
    detail_url=detail_url+(mid)
    headers['Cookie']=get_random_cookie(cookie_pool)
    res=requests.get(detail_url,headers=headers).text
    soup = BeautifulSoup(res, "html.parser")
    script=str(soup.find_all('script')[1])
    
    detail={}
    detail['微博账号']=re.findall(r'"screen_name":(.*?),',script)
    detail['发布时间']=re.findall(r'"created_at":(.*?),',script)
    detail['发布微博']=re.findall(r'"text":(.*?),',script)  #需要做数据清洗
    detail['转发数']=re.findall(r'"reposts_count":(.*?),',script)
    detail['评论数']=re.findall(r'"comments_count":(.*?),',script)
    detail['点赞数']=re.findall(r'"attitudes_count":(.*?),',script)
    return detail

def prase_comment(url,i,payload):
    aim_url_child='https://m.weibo.cn/comments/hotFlowChild'
    cookie=get_random_cookie(cookie_pool)
    headers['Cookie']=cookie
    proxy=get_random_proxy(proxy_pool)

    res=requests.get(url,headers=headers,params=payload,proxies=proxy)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"正在爬取第",i+1,"页评论")
    print("using cookie:",cookie[-24:],"    using proxy:",proxy['proxy'])
    # 处理JSON格式的数据
    # json.dumps将ptyhon的dict转成str
    # json.loads将str转成python的dict类型
    if(is_json(res.content)):
        res=res.content
        con=json.loads(res)
        if(con['ok']==0):
            time_end=time.time()
            print('！！已经爬完全部了?time cost',time_end-time_start,'s')
            os._exit(0)
        l=len(con['data']['data'])
        text_comm[str(i+1)]="第"+str(i+1)+"页评论"#方便在json文件中查找

        for x in range(0,l): 
            uid=con['data']['data'][x]['id']
            uid=str(uid)
            name=con['data']['data'][x]['user']['screen_name']
            comm_text=con['data']['data'][x]['text']
            comment_time=con['data']['data'][x]['created_at']
            like_count=con['data']['data'][x]['like_count']
            text_comm[uid]={}
            text_comm[uid][name]=comm_text
            text_comm[uid]['评论时间']=comment_time
            text_comm[uid]['点赞数']=like_count
            # 對內容進行解析,如果其rootid作為参数cid 发起请求返回为json,则开始对评论的评论进行爬取
            cid=con['data']['data'][x]['rootid']
            payload_child={
                'cid':cid,
                'max_id':None,
                'max_id_type':0
            }

            # 破案了,一个requests.get过去差不多就是10s  因为使用了蓝灯。。。          
            res=requests.get(aim_url_child,headers=headers,params=payload_child).content
            if(is_json(res)):
                con_pre=json.loads(res)
    
                if(con_pre['ok']==0):
                    print("     ","本评论并无子评论")
                    continue
                else:
                    print("     ","爬取子评论中")
                    for ii in range(0,6):       
                        mes=prase_comment_child(aim_url_child,ii,payload_child,cid)
                        if(isinstance(mes,int)):
                            break
                        else:
                            payload_child=mes[0]
                    
        # 每爬完一页开始写入json文件
        jsObj=json.dumps(text_comm, ensure_ascii = False)
        fileObj=open('data1.json','w',encoding='utf-8')
        fileObj.write(jsObj)
        fileObj.close() 
        # 获取max_id作为下次请求的参数
        max_id=con['data']['max_id']  
        if(max_id!=0):   
            payload={
                'id':mid,
                'max_id':max_id,
                'max_id_type':0,
                'mid':mid
            }
            return max_id,payload
        else:
            time_end=time.time()
            print('！！已经爬完全部了 time cost',time_end-time_start,'s')
            os._exit(0)

    # 不是json对象,就要看看是什么
    else:
        print(res.text)
        time_end=time.time()
        print('"哦豁,完蛋！GG !time cost',time_end-time_start,'s')
        os._exit(0)
    
def prase_comment_child(url,i,payload,cid):
    cookie=get_random_cookie(cookie_pool)
    headers['Cookie']=cookie
    proxy=get_random_proxy(proxy_pool)
    # 如果子评论到底了,做个退出操作,应该是没有max_id了
    res=requests.get(url,headers=headers,params=payload,proxies=proxy)
    print("     ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"正在爬取第",i+1,"页子评论")
    print("     ","using cookie:",cookie[-24:],"    using proxy:",proxy['proxy'])
    
    if(is_json(res.content)):
        res=res.content
        con_child=json.loads(res)
        l=len(con_child['data'])
        # 提取一页中想要的信息
        for x in range(0,l): 
            uid=con_child['data'][x]['id']
            uid=str(uid)
            name=con_child['data'][x]['user']['screen_name']
            comm_text=con_child['data'][x]['text']
            comment_time=con_child['data'][x]['created_at']
            like_count=con_child['data'][x]['like_count']

            text_comm[uid]={}
            text_comm[uid][name]=comm_text
            text_comm[uid]['评论时间']=comment_time
            text_comm[uid]['点赞数']=like_count
   
        # 每爬完一页开始写入json文件
        jsObj=json.dumps(text_comm, ensure_ascii = False)
        fileObj=open('data1.json','w',encoding='utf-8')
        fileObj.write(jsObj)
        fileObj.close() 

        # 获取max_id作为下次请求的参数
        max_id=con_child['max_id']
        if(max_id!=0): 
            payload_child={
                'cid':cid,
                'max_id':max_id,
                'max_id_type':0
                }
        else:
            print("      ！！子评论爬到底了")
            return max_id
    else:
        time_end=time.time()
        print(res.text)
        print('哦豁,完蛋! GG time cost',time_end-time_start,'s')
        os._exit(0)
    return payload_child,max_id

if __name__=="__main__": 
    time_start=time.time()
    # 每次爬取前将json文件内容清空
    clean_json()
    # 更新cookie池 代理池
    proxy_pool=get_proxy_pool()
    cookie_pool=get_cookie_pool()
    time_end=time.time()
    print("refresh cookie_pool cost:",time_end-time_start)
    # 可做 :通过键盘来输入mid,即weibo_detail id
    detail_url='https://m.weibo.cn/detail/'
    aim_url='https://m.weibo.cn/comments/hotflow'
    # mid就是微博内容id
    mid=4303451069995022  
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Cookie': None,
        'Host': 'm.weibo.cn'
     }
    payload={
          'id':mid,
          'max_id':None,
          'max_id_type':0,
          'mid':mid
      } 
    text_comm={} 
    detail=prase_weibo(str(mid))
    for key in detail.keys():
        val=detail[key][0]
        print(key+':'+val)

    for i in range(0,20):
        mes=prase_comment(aim_url,i,payload)
        payload=mes[1]
        max_id=mes[0]
        if(max_id==0):
            break
          # sleep_time=3*(random.random())
          # time.sleep(sleep_time) #随机休眠0-3秒
    #计算爬虫总共运行时间,如果它半途不挂掉的话是会运行到这里来的。。。 
    time_end=time.time()
    print('time cost',time_end-time_start,'s')


# baidu ua:Baiduspider+(+http://www.baidu.com/search/spider.htm)
# 还需要一个模拟登陆模块
# 以下为通过api爬取评论的代码

# cookie='_T_WM=c266497ccd9f46eb7e0024ee107e4999; SUB=_2A2525cKsDeRhGeBK6VIU8ifKzz2IHXVSKe7krDV6PUJbkdAKLWetkW1NR_acLmTxMl84UPqCDnu9pugw-bfa9bGK; SUHB=06ZFq5wt0WDev7; SCF=AplbpD-69usWOKAGawEkdJnwO8js07P4C0Qll3d9IRkbwdrh01Dfj4meK87eNiI2NK9VfhWPcRD_Krkm1Kw3gt0.; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D10000011%26fid%3D100103type%253D1%2526q%253D%25E7%258E%258B%25E6%2580%259D%25E8%2581%25AA'
# headers={
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
#         'Cookie': cookie,
#         'Host':'m.weibo.cn'
#         # 'Referer':'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F'
#     }

# urls = ['https://m.weibo.cn/api/comments/show?id=4303451069995022&page={}'.format(str(i)) for i in range(0,1000)]
# comm_dict={}
# for url in urls:
#     res=requests.get(url,headers=headers)
#     print(res.status_code,"ok") 
#     if(res.status_code!=200):
#         print("woc不让我爬")
#         continue
#     else:
#         print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"正在爬取第",int(url[62:len(url)])+1,"页评论")
#         data=res.content
#         con=json.loads(data.decode("utf-8","ignore"))
#     #返回的json数据,该如何提取
#         l=len(con['data']['data'])
#         for i in range(0,l):
#             screen_name=con['data']['data'][i]['user']['screen_name']
#             comm_dict[screen_name]=con['data']['data'][i]['text']
#             jsObj=json.dumps(comm_dict, ensure_ascii = False)
#             fileObj=open('data4.json','w',encoding='utf-8')
#             fileObj.write(jsObj)
#             fileObj.close()
#         time.sleep(1) 
# time_end=time.time()
# print('time cost',time_end-time_start,'s')


# comment_api只允许爬取100页评论

# 删掉前面的信息,分词时候只保留具体评论
# 可存储下评论人\评论时间\评论
# 显示具体微博信息,如点赞数量,转发数量,评论数量等,不用api

# 出错处理,判断是否返回200？判断返回的内容是否是带数据的json,若不是,则跳过本轮
# 对出错处理的退出理解,跳到上一层




