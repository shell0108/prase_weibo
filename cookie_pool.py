import requests
import time
import random

def get_cookie_pool():
    pre_cookie='_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803'
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Cookie':pre_cookie,
    'Referer':'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F'
        }

    login_url='https://passport.weibo.cn/sso/login'
    # 账号和密码可从txt文件中读取
    f = open("xiaohao.txt","r",encoding='utf-8') 
    lines = f.readlines()      #读取全部内容 ，并以列表方式返回
    username_list=[]
    password_list=[]
    cookie_pool={}

    l=len(lines)
    for i in range(0,l):
        usermes=lines[i]
        usermes2=usermes.split(' ')
        username_list.append(usermes2[0])
        password_list.append(usermes2[1])
    for i in range(0,l):
        username=username_list[i]
        password=password_list[i]
        post_data={
            'entry':'mweibo',
            'username':username,
            'password':password
        }
        res=requests.post(login_url,headers=headers,data=post_data) #发出post请求成功登陆
        raw_cookie=res.headers['Set-Cookie'].split(';')
        SUB=raw_cookie[0]
        SHUB=raw_cookie[4].split(',')[1]
        SCF=raw_cookie[7].split(',')[1]
        SSOLoginState=raw_cookie[-3].split(',')[1]

        cookie=pre_cookie+";"+SUB+";"+SHUB+";"+SCF+";"+SSOLoginState
        # 最后将MLOGIN=0 改为MLOGIN=1
        cookie=cookie.replace("MLOGIN=0","MLOGIN=1")
        cookie_pool[str(i)]=cookie
        sleep_time=3*(random.random())
        time.sleep(sleep_time) #随机休眠0-3秒

    return cookie_pool

def get_random_cookie(cookie_pool):
    l=len(cookie_pool)-1
    r=str(random.randint(0,l))
    cookie=cookie_pool[r]
    return cookie





