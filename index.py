# 导入运行库
import websocket
import os
import json
import importlib
import sys
import time
import subprocess
#导入Flask
from flask import Flask
from flask import request
# 导入Prompt_toolkit
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.controls import BufferControl
# 导入libs本地库
from libs import logger
from libs import thread
from libs import loadplugin
from libs import check
from libs import dellib
from libs import maxm
# 环境变量
version = "BETA-0.3"  # 版本信息
level = 1  # 日志等级
host="localhost" # 请求host
http_host="localhost" #监听器HTTP host(可选)
serv_port = "5705"  # 监听器PORT
send_port = "5700"  # 请求PORT
run_cq_args = ""  # cqhttp启动命令
bot_mode="WS:HTTP" # 驱动器选择
AuthToken="" # 验证Token
loadType="reload" # 加载器模式(create/reload)
# 创建主窗口
buffer1 = Buffer(name="main")
# 创建日志
log = logger.Logger("Main", level, buffer1)
# 创建命令输入窗口
buffer2 = Buffer(multiline=False)
# 设置窗口布局
root_container = HSplit(
    [Window(content=BufferControl(buffer=buffer1)), Window(content=BufferControl(buffer=buffer2), height=1)])
layout = Layout(root_container)
# 设置按键绑定
kb = KeyBindings()
# 配置窗口程序
app = Application(full_screen=True, key_bindings=kb, layout=layout)

# 获取disloads
def getpdl():
    with open("./config/bot/disloads.pdl", "r") as f:
        return f.readlines()


# 命令系统
def userinput(text):
    log = logger.Logger("UserInput", level, buffer1)
    log.info(text)
    with open("./config/bot/commands.cdl", "r") as f:
        commands = f.readlines()
    unloadlist = getpdl()
    for a in commands:
        a = a.replace("\n", "").split("|")
        if text.split(" ")[0] == a[0]:
            pluginslist = os.listdir("./plugins")
            for i in pluginslist:
                name = i.split(".")[0]
                if unloadlist.count("%s\n" % i) == 0 and i != "__pycache__":
                    if loadType=="create":
                        plugin = importlib.import_module("plugins." + name)
                        if a[1] == plugin.main.name:
                            thread.create(loadplugin.runPlugin,
                                      (plugin, logger.Logger(plugin.main.name, level, buffer1), "commands", 0, text))
                    elif loadType=="reload":
                        modules = sys.modules.copy()
                        if list(modules.keys()).count("plugins.%s" % name):
                            plugin = modules["plugins.%s" % name]
                        else:
                            plugin = importlib.import_module("plugins." + name)
                        if a[1] == plugin.main.name:
                            thread.create(loadplugin.runPlugin,
                                      (plugin, logger.Logger(plugin.main.name, level, buffer1), "commands", 0, text))

def regcommand(major, name):
    with open("./config/bot/commands.cdl", "a") as f:
        f.write("%s|%s\n" % (major, name))
# 监听按键绑定
@kb.add('c-q')  # event:ctrl+q
def _(event):
    app.output.bell()
    app.exit()  # 退出程序
@kb.add("enter")  # event:enter
def _(event):
    if buffer2.text:
        buffer2.append_to_history()
        userinput(buffer2.text)
        buffer2.reset()


# 聚焦到命令窗口
app.layout.focus(buffer2)

# 加载插件
def llPlugin(data):
    pluginslist = os.listdir("./plugins")
    unloadlist = getpdl()
    for i in pluginslist:
        name = i.split(".")[0]
        if unloadlist.count("%s\n" % i) == 0 and i != "__pycache__":
            if loadType=="create": # 适配于BETA-0.2以前的插件
                plugin = importlib.import_module("plugins." + name)
                thread.create(loadplugin.runPlugin,
                          (plugin, logger.Logger(plugin.main.name, level, buffer1), data["post_type"], data))
            elif loadType=="reload": # BETA-0.3新特性,可改善性能优化开发流程
                modules=sys.modules.copy()
                if list(modules.keys()).count("plugins.%s"%name):
                    plugin=modules["plugins.%s"%name]
                else:
                    plugin = importlib.import_module("plugins." + name)
                thread.create(loadplugin.runPlugin,
                              (plugin, logger.Logger(plugin.main.name, level, buffer1), data["post_type"], data))




# websocket正向驱动器
def main():
    ws=websocket.WebSocket()
    if AuthToken:
        ws.connect("ws://%s:%s"%(host,serv_port),header={"Authorization":AuthToken})
    else:
        ws.connect("ws://%s:%s" % (host, serv_port))
    while True:
        message=ws.recv()
        if message:
            list=[]
            data = json.loads(message)
            for i in data.keys():
                list.append(i)
            if list.count("post_type") and data["post_type"] != "meta_event":
                thread.create(llPlugin, (data,))
            elif list.count("echo"):
                with open("./cache/websocket.rpl","a",encoding="utf-8")as f:
                    f.write(data+"\n")
    def send(data):
        ws = websocket.WebSocket()
        ws.connect(host)
        ws.send(str(data))
        ws.close()
#HTTP反向驱动器
def httpserver():
    app = Flask(__name__)

    @app.route('/', methods=["POST"])
    def _():
        thread.create(llPlugin, (request.get_json(),))
        return ""
    if http_host:
        app.run(host=http_host, port=int(serv_port))
    else:
        app.run(host=host, port=int(serv_port))
def runServer():
    if run_cq_args:
        log.info("等待go-cqhttp启动,静置10s")
        time.sleep(10)
    mode=bot_mode.split(":")[0]
    if check.serv_lock():
        if mode=="WS":
            thread.create(main())
        elif mode=="HTTP":
            thread.create(httpserver())
    else:
        if mode=="HTTP":
            log.warning("开发者锁定驱动器模式为WS:HTTP,将使用WS正向连接")
        thread.create(main())
# CQHTTP子进程
def CQHTTP():
    log = logger.Logger("go-cqhttp", level, buffer1)
    if run_cq_args:
        log.info("创建go-cqhttp子进程")
        cmd = subprocess.Popen(run_cq_args, cwd="./go-cqhttp", encoding="utf-8", stdout=subprocess.PIPE, shell=True)
        for M in cmd.stdout:
            log.info(M.split(":", 3)[len(M.split(":", 3))-1].replace("\n", ""))


# 初始化指令
def initcommand():
    with open("./config/bot/commands.cdl", "w") as f:
        f.write("")


# 初始化插件
def initPlugins():
    pluginslist = os.listdir("./plugins")
    for i in pluginslist:
        name = i.split(".")[0]
        unloadlist = getpdl()
        if unloadlist.count("%s\n" % i) == 0 and i != "__pycache__":
            plugin = importlib.import_module("plugins." + name)
            if not os.listdir("./config").count(plugin.main.name):
                os.mkdir(f"./config/{plugin.main.name}")
            thread.create(loadplugin.runPlugin,
                          (plugin, logger.Logger(plugin.main.name, level, buffer1), "init", 0))
# 清理缓存
def clearCache():
    dellib.delpath("./cache")
    os.mkdir("./cache")
# 启动内存限制(Unix专有模块,非Unix请不要使用本模块)
def killmx():
    args=sys.argv
    for i in args:
        if i.find("-Kmx")==0:
            mxm=i.replace("-Kmx","")
            if mxm and mxm.isdigit():
                log.warning("最大虚拟内存限制为%sMiB"%mxm)
                maxm.limit_memory(1024*1024*int(mxm))
            else:
                log.error("启动参数错误")
# 初始化
def init():
    logo = """
            ====================================================================

                  /$$$$$$  /$$                                  /$$$$$$ 
                 /$$__  $$|__/                                 /$$__  $$
                | $$  \__/ /$$ /$$$$$$/$$$$   /$$$$$$         | $$  \ $$
                |  $$$$$$ | $$| $$_  $$_  $$ /$$__  $$ /$$$$$$| $$  | $$
                 \____  $$| $$| $$ \ $$ \ $$| $$  \ $$|______/| $$  | $$
                 /$$  \ $$| $$| $$ | $$ | $$| $$  | $$        | $$/$$ $$
                |  $$$$$$/| $$| $$ | $$ | $$| $$$$$$$/        |  $$$$$$/
                 \______/ |__/|__/ |__/ |__/| $$____/          \____ $$$
                                            | $$                    \__/
                                            | $$                        
                                            |__/                        

            ====================================================================
            """
    log.info(logo)
    check.Check()
    log.info(f"SimpQ-Ref {version} is Running")
    killmx()
    initcommand()
    initPlugins()
    clearCache()

# 启动屏幕应用
def runapp():
    app.run()
    sys.exit()


if __name__ == "__main__":
    # 启动GO-CQHTTP
    thread.create(CQHTTP, ())
    # 启动窗口
    thread.create(runapp, ())
    # 初始化框架
    init()
    # 启动监听器
    runServer()
