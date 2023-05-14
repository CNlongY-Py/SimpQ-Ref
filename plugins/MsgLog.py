class main:
    name = "MsgLog"
    author = "CNlongY"
    version = "0.0.1"

    def __init__(self, raw_json, sub_type, log, bot, index):
        self.raw_json = raw_json
        self.sub_type = sub_type
        self.log = log
        self.bot = bot
        self.index = index

    def init(self):
        self.log.info(f"{main.name}插件 {main.version} 初始化 by:{main.author}")
        self.log.info("当前登录号信息 %s(%s)"%(self.bot.get_login_info()["nickname"],self.bot.get_login_info()["user_id"]))
        self.index.regcommand("send", main.name)
    def message(self):
        log=self.log
        bot=self.bot
        sub_type=self.raw_json["message_type"]
        if sub_type == "group":
            group_id=self.raw_json["group_id"]
            user_id=self.raw_json["user_id"]
            message=self.raw_json["message"]
            groupName=bot.get_group_info(group_id)["group_name"]
            userName=bot.get_group_member_info(group_id,user_id)["nickname"]
            log.info(f"[群聊消息]<{groupName}>{userName}:{message}")
        elif sub_type == "private":
            user_id=self.raw_json["user_id"]
            message=self.raw_json["message"]
            userName=bot.get_stranger_info(user_id)["nickname"]
            log.info(f"[私聊消息]<{userName}>:{message}")
    def notice(self, notice_type):
        pass

    def request(self, request_type):
        pass

    def commands(self, txt):
        args=txt.split(" ",1)[1].split(":")
        self.bot.send_group_msg(group_id=args[0],message=args[1])
        self.log.info("发送到群%s(%s):%s"%(self.bot.get_group_info(group_id=args[0])["group_name"],args[0],args[1]))

