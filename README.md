# SimpQ-Ref
![LOGO](https://github.com/CNlongY-Py/SimpQ-Bot/blob/main/doc/LOGO23-4.png)

![Onebot](https://img.shields.io/badge/OneBot-11-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==)
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
