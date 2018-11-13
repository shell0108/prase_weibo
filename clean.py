import json
import re
import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image

# with open("data4.json",'r',encoding='utf-8') as data:
#     comm_dict=json.load(data)#将json对象变为了一个字典
#     # 对其进行数据清洗,首先去除掉回复
#     for key in comm_dict.keys():
#     # 共200条,注意直接遍历value没有效果,修改value还需遍历key
#         val=comm_dict[key]
#         if((val[0:2])=='回复'): #清除回复
#             val=val.split(':')
#             comm_dict[key]=val[2] 
#             # 清除span和a标签
#         pat=r'<span (.*?)>(.*?)</span>'
#         comm_dict[key]=re.sub(pat,"",comm_dict[key])
#         pat2=r'<a (.*?)>(.*?)</a>'
#         comm_dict[key]=re.sub(pat2,"",comm_dict[key])
#         val2=comm_dict[key].split('<')
#         comm_dict[key]=val2[0]

# jsObj=json.dumps(comm_dict, ensure_ascii = False)    
# fileObj=open('data5.json','w',encoding='utf-8')
# fileObj.write(jsObj)
# fileObj.close()

with open("data5.json",'r',encoding='utf-8') as data:
    comm_dict=json.load(data)#将json对象变为了一个字典
    comm_list=[]
    for value in comm_dict.values():
        if((value.strip())!=''):
            comm_list.append(value)
    l=len(comm_list)
    comm_list_fenci=[]
    for i in range(0,l):
        g=jieba.cut(comm_list[i],cut_all=False)
        for n in g:
            # 清除掉空白字符以及中文逗号
            if(n.strip()!=''):
                if(n!='，'):
                    if(n!='ig'):
                        if(n!='IG'):
                            comm_list_fenci.append(n) 
    #列表,现在将其拼接为字符串
    fenci=' '.join(comm_list_fenci) 
    file = open('test.txt','w',encoding='utf-8')
    file.write(fenci)
    file.close()

    im = np.array(Image.open('ignb.png'))
    #Generate WordCloud
    wc=WordCloud(background_color = "white",
                max_words = 100,
                mask = im,
                max_font_size = 80,
                font_path = 'msyh.ttf')
    wc.generate(fenci)
    # 从背景图片得到颜色
    imColor = ImageColorGenerator(im)  

    plt.imshow(wc)
    plt.axis("off")
    plt.figure()
    plt.imshow(wc.recolor(color_func=imColor))
    plt.axis("off")
    plt.figure()







