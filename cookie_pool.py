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

def get_random_cookie():
    # cookie_pool={'0': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pBFDeRhGeBK6VIS8CbKyjyIHXVSFDANrDV6PUJbkdBeLRfYkW1NR_acLVClL83aycfv6UZwBrDkvxceyuXB; SUHB=0qj0skSvu6pUz8; SCF=AkTDxAEkHlZkvlvzXL5JBt_FrPGRV4NwjUeTB-KiHilctSjznDaJ_0VEJ6l9tJzqh_mLydpgvyT2l4ismLxk00A.; SSOLoginState=1542381589', '1': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pBIDeRhGeBK6VIU8ifKzz2IHXVSFDAArDV6PUJbkdBeLXDekW1NR_acLjU0ldRG3c76Z2_r_1AecczDKQfp; SUHB=0IIVNny20hoMB0; SCF=Aj10RDf_8jD1B471kX8qjMxUH4Ac05X2mosqPFTJhj6-nUgpKx2_Rh8Ujl1pLN1IVj-XbKTKnXIe251Ap9WLTqM.; SSOLoginState=1542381592', '2': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pBJDeRhGeBK6lAV9ifKzjuIHXVSFDABrDV6PUJbkdBeLVTDkW1NR_acFWGqbb80pf4JszDYR-Z7Xq2XiMFv; SUHB=0idrimZeV106Tt; SCF=At33MmzJzmbYcHI5hi6qasZBpjnMGqqzXZAPS0iB5f7eybnuFnf-1VC5aD84KGtV0pQZUdS2jkBY9g5eB_X3RgU.; SSOLoginState=1542381594', '3': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pBMDeRhGeBK6lAW9SrKzDqIHXVSFDAErDV6PUJbkdBeLXn5kW1NR_acEILoJDctG6B9vyaDdcsALjQ2KjY2; SUHB=08J7w3zcIyYwmn; SCF=AklhHKBWxNTkOuAl5-3wklU0eDdrNgLZpu0EU2GL5kADo6m0pTKHtbgLETyEUay7QeNo3ZqNIC-ZqWTHQGkJQtw.; SSOLoginState=1542381596', '4': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pBwDeRhGeBK6lAW9SrKzDuIHXVSFDA4rDV6PUJbkdBeLRLMkW1NR_acEC_yV8cCT3UYJsj-g8RNdIs1oZdY; SUHB=010GNzud_bEQhC; SCF=Aj6_9kyiZNsqD6cUmseFJtTxspYygUz5dTckOBxW2Soh1nUCfPS4ExhnauQR5fD4LkrDYho3NUxed1GI3oCC23Q.; SSOLoginState=1542381600', '5': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pByDeRhGeBI4lcX9C3JyDmIHXVSFDA6rDV6PUJbkdBeLUHxkW1NRkVIEAL0yB-ifu5Te7lVgC3SiUqzc0vC; SUHB=0btssHPaLc42hI; SCF=AmIfTctKfohhdQDU7tQe2nNn9lvMb3YyBiI17NxmyK228wAYt9tmx1My_BF9NgJfHyxtfEODFt5Ti7eLXOKgA18.; SSOLoginState=1542381602', '6': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pB0DeRhGeBI4lcX9C3KyT-IHXVSFDA8rDV6PUJbkdBeLWiikW1NRkVIMgat4xaiW5xLwUGLbhMxvLn-kdPh; SUHB=0oU4tStYtGtt95; SCF=Ajq9uuh1avmM8AwloCg8iE3wsHE_Vwked-iGZj1Z4GzIQQlNEEQYQKrnjhWc8IoPF63HbvXA2p1Q5RmjtPnTudg.; SSOLoginState=1542381605', '7': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pB2DeRhGeBJ6VsQ8SbOzT2IHXVSFDA-rDV6PUJbkdBeLUzGkW1NRkVIMjkgFQWldNVV6EwS_M6ge_dDiYeT; SUHB=0vJYySkReWEkoX; SCF=Ahdw2HCFvFLXrnzMg3RTkEtWM1AoVWug7YEndBM0yXGaavwFHsu_4-4l-ZfK8mZEHJocNfGO5217nhrqIVtePD0.; SSOLoginState=1542381606', '8': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pB4DeRhGeBI4lcY9CrKyz2IHXVSFDAwrDV6PUJbkdBeLWrNkW1NRkVIOklNTuqMGDdBVwx13e7eAySsozHd; SUHB=0cS3uNjUjz9Je5; SCF=AkX7FPHEEJufmYVOC9Uo6al2hcGnkNaE2KKYDOfWpB8CPqqKNrb8Q7YgVxO00Vi11Wmza8RBX0BP3nAa-k4dm88.; SSOLoginState=1542381608', '9': '_T_WM=c266497ccd9f46eb7e0024ee107e4999;  WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode=10000011&fid=102803;SUB=_2A2526pB8DeRhGeBI4lcY9CrKzjWIHXVSFDA0rDV6PUJbkdBeLXbWkW1NRkVIyAoQ3Kk3v_LD0s7Div-DtK20q-Uh; SUHB=0mxE35LmbArx0U; SCF=AhvuIYa0x7T7QG-DtSFIUvIX6Nsi5v68Smk3bJKWYrkN9eIhrOw2GHFL4s3ZgCcgBuK74pEugKaNCKrDZE8HGu0.; SSOLoginState=1542381612'}
    l=len(cookie_pool)-1
    r=str(random.randint(0,l))
    cookie=cookie_pool[r]
    return cookie

# print(get_cookie_pool())



