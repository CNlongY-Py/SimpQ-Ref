import importlib
import traceback

def runPlugin(getPlugin, log, type, rjson, txt=0):  # 为插件创建线程
    try:
        bot = importlib.import_module("libs.api")
        if type!="message":
            bot = bot.API(
                uid=0,
                gid=0,
                mid=0,
                plugin=getPlugin.main.name,
            )
        else:
            bot = bot.API(
                uid=rjson["user_id"],
                gid=rjson["group_id"],
                mid=rjson["message_id"],
                plugin=getPlugin.main.name,
            )
        if type == "message":
            main = getPlugin.main(
                sub_type=rjson["sub_type"],
                raw_json=rjson,
                log=log,
                bot=bot,
                index=importlib.import_module("index"),
            )
            main.message()
        elif type == "notice":
            main = getPlugin.main(
                sub_type=0,
                raw_json=rjson,
                log=log,
                bot=bot,
                index=importlib.import_module("index"),
            )
            main.notice(rjson["notice_type"])
        elif type == "request":
            main = getPlugin.main(
                sub_type=0,
                raw_json=rjson,
                log=log,
                bot=bot,
                index=importlib.import_module("index"),
            )
            main.request(rjson["request_type"])
        elif type == "init":
            main = getPlugin.main(
                sub_type=0,
                raw_json=0,
                log=log,
                bot=bot,
                index=importlib.import_module("index"),
            )
            main.init()
        elif type == "commands":
            main = getPlugin.main(
                sub_type=0,
                raw_json=0,
                log=log,
                bot=bot,
                index=importlib.import_module("index"),
            )
            main.commands(txt)
    except:
        log.error("\n %s"%traceback.format_exc())
