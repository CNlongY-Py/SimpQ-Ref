# SimpQ-Ref
![LOGO](https://github.com/CNlongY-Py/SimpQ-Bot/blob/main/doc/LOGO23-4.png)

SimpQ-Ref为SimpQ的分支版本
相较于SimpQ-Bot,SimpQ-Ref拥有更多的功能,更优雅的界面


## **请务必加入社区群以此获取最新Snapshot**
QQGroup:[SimpQ 社区 556990446](https://qm.qq.com/cgi-bin/qm/qr?k=d5jHYYrg1XkSwuvItCCWfWxcALOxqAeM&jump_from=webapi&authKey=Qtw/AoANvNmCcSeSH9IqafXqbToZRE5aFuUtZuWJpKMmVaALfw2P9zp8orX6czjZ)



# 开始

**python版本建议使用3.10.9**

安装运行程序所需的Package
```
pip install requests
pip install flask
pip install prompt_toolkit
pip install websocket-client
```

下载合适的go-cqhttp版本放入go-cqhttp文件夹中https://github.com/Mrs4s/go-cqhttp/releases

将config.yml中uin和password修改即可

遇到登录错误看这篇issues-->https://github.com/Mrs4s/go-cqhttp/issues/2053

将go-cqhttp填入index.py中run_cq_args变量(Windows:go-cqhttp_xxx_xxx.exe Linux:go-cqhttp)

启动index.py **(使用shell启动)**

***SimpQ-Ref已经启动了,编写属于你自己的Bot吧***

API文档https://docs.go-cqhttp.org/api/ (终结点为函数名称)
