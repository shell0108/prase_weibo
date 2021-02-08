# prase_weibo
爬取微博移动端某条评论下的内容以及某个大v的粉丝信息

思路:
先通过爬取每个大V的粉丝列表，获得每个粉丝的id与名称将其存入fans_id.json
![](pics/get_fans_id.png)
将fans_id.json拆分成几个小文件后,启动多线程对每个文件中粉丝id去爬取粉丝主页
并将最终的数据存取到数据库中