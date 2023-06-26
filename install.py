import pip
import time
import os
import requests
version="Snapshot-3y6m26d"
print(f"SimpQ Toolkit {version} is Running")
print("正在检查安装环境")
if len(os.listdir("./"))>2:
    print("非空文件夹,请将本文件放置于空文件夹安装")
else:
    print("正在检查网络链接")
    if requests.get("https://raw.githubusercontent.com/CNlongY-Py/SimpQ-Ref/main/LICENSE"):
        print("正在准备下载")
        img=requests.get("https://raw.githubusercontent.com/CNlongY-Py/SimpQ-Ref/main/install.img").json()
        url=img["url"]
        print("正在安装需要的库")
        for i in img["package"]:
            print(f"正在安装 {i}")
            pip.main(["install",i])
        print("正在新建文件夹")
        for i in img["folder"]:
            print(f"正在创建 {i}")
            os.mkdir(i)
        print("正在下载必要文件")
        for i in img["file"]:
            print(f"正在下载 {i}")
            with open(i,"w")as f:
                f.write(requests.get(f"{url}{i}").text)
        print("正在创建许可证")
        with open("config/bot/.UNLOCKED","w")as f:
            stime=time.strftime("3y%mm%dd", time.localtime())
            license=f"SimpQ-Ref {stime}许可证\n来源于install {version}安装"
            f.write(license)
        print("安装完成!")    