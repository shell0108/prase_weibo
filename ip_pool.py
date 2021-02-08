import requests
import random
import json

def get_proxy_pool():
    res=requests.get('http://lab.crossincode.com/proxy/get/?num=20') 
    con=res.content
    # 变成字典 全部提取代理ip
    con=json.loads(res.content)
    proxy_pool={}
    for i in range(0,20):
        proxy_pool[i]=con['proxies'][i]['http']
    # proxy为字符串
    return proxy_pool


def get_random_proxy():
    i=random.randint(1,20)
    proxy=proxy_pool[i-1]
    proxy = {
    'proxy': 'http://'+proxy
    }
    return proxy



    





