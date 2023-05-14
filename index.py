# 导入运行库
import asyncio
import websocket
import os
import json
import importlib
import sys
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

# 环境变量
version = "BETA-1.0"  # 版本信息
level = 1  # 日志等级
host="localhost" # 请求host
http_host="localhost" #监听器HTTP host(可选)
serv_port = "5700"  # 监听器PORT
send_port = "5701"  # 请求PORT
run_cq_args = ""  # cqhttp启动命令
bot_mode="WS:HTTP" # 驱动器选择
# 创建主窗口
buffer1 = Buffer()
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
def userinput(text, log):
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
        userinput(buffer2.text, logger.Logger("Command", level, buffer1))
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
            plugin = importlib.import_module("plugins." + name)
            thread.create(loadplugin.runPlugin,
                          (plugin, logger.Logger(plugin.main.name, level, buffer1), data["post_type"], data))




# websocket正向驱动器
def main():
    print("[Warning]Websocket正在运行,按下Ctrl+C断开")
    ws=websocket.WebSocket()
    ws.connect("ws://%s:%s"%(host,serv_port))
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
    print("[Warning]HTTP监听器正在运行,按下Ctrl+C断开")
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
# 递归删除文件
def delpath(path):
    if os.path.isdir(path):  # 判断是不是文件夹
        for file in os.listdir(path):  # 遍历文件夹里面所有的信息返回到列表中
            clearCache(os.path.join(path, file))  # 是文件夹递归自己
        if os.path.exists(path):  # 判断文件夹为空
            os.rmdir(path)  # 删除文件夹

    else:
        if os.path.isfile(path):  # 严谨判断是不是文件
            os.remove(path)  # 删除文件
# 清理缓存
def clearCache():
    delpath("./cache")
    os.mkdir("./cache")
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
