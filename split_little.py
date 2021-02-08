import json

def split_little(n):
    with open("fans_id.json",'r',encoding='utf-8') as jsObj:
        fans_dict=json.load(jsObj)
        l=len(fans_dict)
        count=1
    fans_dict={}
    for line in open("fans_id.json",'r',encoding='utf-8'):  
        fans_dict[line[5:15]]=line[19:-4]
        count=count+1    
        for i in range(0,n):
            if(count>(i+1)*(l/n)):
                if(count<((i+1)*(l/n)+1)):
                    json_file="fans_id"+str(i+1)+".json"   
                    fileObj=open(json_file,'w',encoding='utf-8')           
                    jsObj=json.dumps(fans_dict, ensure_ascii = False)
                    fileObj.write(jsObj)
                    fileObj.close() 
                    fans_dict={}   

    # 怎么会有bug导致第一行为空的？？？？？
    with open("fans_id1.json","r",encoding="utf-8") as jsObj1:
        fans_dict=json.load(jsObj1)
        fans_dict.pop('')
        fileObj2=open("fans_id1.json",'w',encoding='utf-8')           
        jsObj=json.dumps(fans_dict, ensure_ascii = False)
        fileObj2.write(jsObj)
        fileObj2.close() 

# n为要拆分成的小文件个数
n = 10
split_little(n+1)
                        




