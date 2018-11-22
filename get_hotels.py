import requests
import json

headers={
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Cookie': 'QN99=7797; QN300=auto_5187810b; QN1=dXrgglvrvzNt8ZMRxQKrAg==; QunarGlobal=10.86.213.149_-32522bbc_16710df08a6_-3fdf|1542176565005; QN205=auto_5187810b; QN277=auto_5187810b; csrfToken=wW4uK7XcdokJ53lZ4EqH8shWk89hERXQ; QN601=b5a84779ebd95cb1c71a27e7d8aa18d9; _i=RBTKSLqokQxVRZVw6HwbAKk7m0Ux; _vi=2T-V4rhTLAl4uuXiV9e41sdfanEkyxcP6UGT7URc0DTTh0pCpJQKHoGQ0AC3Evqf-AEuHUkePtMnbkPH4fswj7bBDuNLX3fpUjxLn7qxzkIvNCzJirIROakhlIUb2M7vfh1QEhrWNvO-8o5cnUkTW77Xfgi3UPvxg_wf0H0zNcuU; QN269=B3F94BF3E7D511E8ADB4FA163E642F8B; QN6=auto_5187810b; QN163=0; QN48=tc_f8eb172708dacb51_16710e2f319_551e; fid=e7a8ace2-5a46-4534-aeec-20ca60de267d; QN271=fe40f606-d8aa-4f57-a738-b585e748201e; QN73=3333-3334; QN70=1cbe0953916710e35520; __utma=183398822.1468800891.1542176597.1542176597.1542176597.1; __utmb=183398822.8.10.1542176597; __utmc=183398822; __utmz=183398822.1542176597.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _jzqa=1.1611638083529514800.1542176600.1542176600.1542176600.1; _jzqb=1.5.10.1542176600.1; _jzqc=1; _jzqx=1.1542176600.1542176600.1.jzqsr=hotel%2Equnar%2Ecom|jzqct=/city/beijing_city/.-; _jzqckmp=1; _RF1=113.54.232.16; _RSG=L5K1ROVmb_Cl5D64tsp0oA; _RDG=28a0a57423efc02b703cfc2fdaddff1f48; _RGUID=cfe5c1f6-1b05-4155-ac80-cf6dc418d16f; QN235=2018-11-14; QN267=208511489dd0c2e78',
        'Host': 'touch.qunar.com',
        'Referer':'https://touch.qunar.com/hotel/hotellist?city=%E5%8C%97%E4%BA%AC&checkInDate=2018-11-14&checkOutDate=2018-11-15&extra=%7B%22L%22%3A%22%22%2C%22DU%22%3A%22%22%2C%22MIN%22%3A0%2C%22MAX%22%3A0%7D'
     }
url='https://touch.qunar.com/api/hotel/hotellist/'
payload={
    'checkInDate':'2018-11-14',
    'checkOutDate':'2018-11-15',
    'extra':{
        "L":" ",
        "DU":" ",
        "MIN":0,
        "MAX":0
    },
    'couponsSelected':-1,
    'city':'北京',
    'page':1
}
hotellist={}
for page_num in range(1,100):
    print("正在爬取第",page_num,"页")  
# ?checkInDate=2018-11-14&checkOutDate=2018-11-15&extra={"L":"","DU":"","MIN":0,"MAX":0}&couponsSelected=-1&city=北京&page=2'
    payload['page']=page_num
    res=requests.get(url,headers=headers,params=payload)
    con=json.loads(res.content)
    l=len(con['data']['hotels'])
    
    for i in range(0,l):
        hotellist[con['data']['hotels'][i]['showAddr']]=con['data']['hotels'][i]['attrs']['hotelName']
        hotel_id=con['data']['hotels'][i]['id']

jsObj=json.dumps(hotellist, ensure_ascii = False)
fileObj=open('hotels.json','w',encoding='utf-8')
fileObj.write(jsObj)
fileObj.close() 
