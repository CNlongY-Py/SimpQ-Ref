import os
import requests
import base64

class main:
    name = "PlugManager"
    author = "CNlongY"
    version = "1.0.1"

    def __init__(self, raw_json, sub_type, log, bot, index):
        self.raw_json = raw_json
        self.sub_type = sub_type
        self.log = log
        self.bot = bot
        self.index = index

    def init(self):
        self.log.info(f"{main.name}插件 {main.version} 初始化 by:{main.author}")
        self.index.regcommand("pm", main.name)

    def message(self):
        pass

    def notice(self, notice_type):
        pass

    def request(self, request_type):
        pass

    def commands(self, txt):
        if len(txt.split(" ")) > 1:
            cmd = txt.split(" ")[0]
            args = txt.split(" ")
            if cmd == "pm":
                type = args[1]
                if type == "unload":
                    name = args[2]
                    self.bot.addpdl(name)
                    self.log.info("卸载%s成功" % name)
                elif type == "load":
                    name = args[2]
                    type = self.bot.delpdl(name)
                    if type:
                        self.log.info("加载%s成功" % name)
                    else:
                        self.log.info("加载%s失败" % name)
                elif type == "list":
                    loads = []
                    for i in os.listdir("./plugins"):
                        if i != "__pycache__" and self.bot.getpdl().count(i.replace(".py", "")) == 0:
                            loads.append(i.replace(".py", ""))
                    self.log.info("当前加载的插件有%s" % loads)
                elif type == "create":
                    type = args[2]
                    name = args[3]
                    if type=="package":
                        os.mkdir("./plugins/%s"%name)
                        with open(self.bot.getcfg("init.py"),"r",encoding="utf-8")as f:
                            py=f.read().replace("{name}",name)
                        with open(f"./plugins/{name}/__init__.py","w",encoding="utf-8")as f:
                            f.write(py)
                        self.log.info(f"{name} 插件包创建完成")
                    elif type=="file":
                        with open(self.bot.getcfg("init.py"), "r",encoding="utf-8") as f:
                            py = f.read().replace("{name}", name)
                        with open(f"./plugins/{name}.py", "w",encoding="utf-8") as f:
                            f.write(py)
                        self.log.info(f"{name} 插件创建完成")
                elif type=="install":
                    url = args[2]
                    data=eval(base64.b64decode(url))
                    self.log.info("PmToken附带文本: %s"%data["text"])
                    for i in data["plugins"]:
                        url=i["url"]
                        name=i["name"]
                        plugpath=url.split("static/")[1]
                        self.log.info(f"正在下载{name}插件至{plugpath}")
                        response=requests.get(url)
                        if response:
                            with open(f"./{plugpath}","wb")as f:
                                f.write(response.content)
                                self.log.info("插件%s安装完成"%url.split("/")[len(url.split("/"))-1])
                        else:
                            self.log.info("请求失败:插件服务器失去连接")