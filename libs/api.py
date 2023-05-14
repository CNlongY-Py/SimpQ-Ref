import time
import json
import index
import requests
from libs import logger
from libs import thread
from libs import check
def websocket(action,args):
    data={"action":action,"params":args,"echo":time.localtime()}
    index.main().send(data)
    def readRpl():
        with open("./cache/websocket.rpl","r",encoding="utf-8")as f:
            for i in f.readlines():
                recv=json.loads(i.replace("\n",""))
                if recv["echo"]==data["echo"]:
                    return recv
    while True:
        recv=readRpl()
        if recv:
            return recv
def http(action,args):
    log = logger.Logger("API", index.level, index.buffer1)
    response=requests.post(f"http://{index.host}:{index.send_port}/{action}",data=args)
    if response:
        return response.json()["data"]
    else:
        log.warning("Bot丢失连接,请检查go-cqhttp状态")
        raise ConnectionError


def api(action, args={}):
    log = logger.Logger("API", index.level, index.buffer1)
    mode=index.bot_mode.split(":")[1]
    if check.serv_lock():
        if mode=="WS":
            return websocket(action,args)
        elif mode=="HTTP":
            return http(action,args)
    else:
        if mode=="WS":
            log.warning("开发者锁定驱动器模式为WS:HTTP,将使用HTTP请求方式")
        return http(action, args)
class API:
    def __init__(self, uid, gid, mid, plugin):
        self.uid = uid
        self.gid = gid
        self.mid = mid
        self.plugin = plugin

    # SimpQ-Ref 内置函数
    def addpdl(self, name):  # 向pdl中添加
        with open("./config/bot/disloads.pdl", "a") as f:
            f.write(name + "\n")

    def delpdl(self, name):  # 删除pdl中文件
        with open("./config/bot/disloads.pdl", "r") as f:
            pdl = f.readlines()
            if pdl.count("%s\n" % name) > 0:
                pdl.remove("%s\n" % name)
                with open("./config/bot/disloads.pdl", "w") as f:
                    f.writelines(pdl)
                return True
            else:
                return False

    def getpdl(self):  # 获取pdl文件
        with open("./config/bot/disloads.pdl", "r") as f:
            pdl = f.read()
            return pdl.split("\n")

    def getcfg(self,path): # 获取cfg中文件
        return "./config/%s/%s"%(self.plugin,path)
    # go-cqhttp函数
    # Bot账号
    def get_login_info(self):
        return api("get_login_info")

    def set_qq_profile(self, nickname, company, email, collage, personal_note):
        return api("set_qq_profile", {"nickname": nickname, "company": company, "email": email, "collage": collage,
                                      "personal_note": personal_note})

    def _get_model_show(self, model):
        return api("_get_model_show", {"model": model})

    def get_online_clients(self, no_cache=False):
        return api("get_online_clients", {"no_cache": no_cache})

    # 好友信息
    def get_stranger_info(self, user_id, no_cache=False):
        return api("get_stranger_info", {"user_id": user_id, "no_cache": no_cache})

    def get_friend_list(self):
        return api("get_friend_list")

    def get_unidirectional_friend_list(self):
        return api("get_unidirectional_friend_list")

    # 好友操作
    def delete_friend(self, user_id):
        return api("delete_friend", {"user_id": user_id})

    def delete_unidirectional_friend(self, user_id):
        return api("delete_unidirectional_friend", {"user_id": user_id})

    # 消息
    def send_private_msg(self, user_id, message, group_id=None, auto_escape=False):
        return api("send_private_msg",
                   {"user_id": user_id, "group_id": group_id, "message": message, "auto_escape": auto_escape})

    def send_group_msg(self, group_id, message, auto_escape=False):
        return api("send_group_msg", {"group_id": group_id, "message": message, "auto_escape": auto_escape})

    def send_msg(self, message_type, user_id, group_id, message, auto_escape=False):
        return api("send_msg",
                   {"message_type": message_type, "user_id": user_id, "group_id": group_id, "message": message,
                    "auto_escape": auto_escape})

    def get_msg(self, message_id):
        return api("get_msg", {"message_id": message_id})

    def delete_msg(self, message_id):
        return api("delete_msg", {"message_id": message_id})

    def mark_msg_as_read(self, message_id):
        return api("mark_msg_as_read", {"message_id": message_id})

    def get_forward_msg(self, message_id):
        return api("get_forward_msg", {"message_id": message_id})

    def send_group_forward_msg(self, group_id, messages):
        return api("send_group_forward_msg", {"group_id": group_id, "messages": messages})

    def send_private_forward_msg(self, user_id, messages):
        return api("send_private_forward_msg", {"user_id": user_id, "messages": messages})

    def get_group_msg_history(self, message_seq, group_id):
        return api("get_group_msg_history", {"message_seq": message_seq, "group_id": group_id})

    # 图片
    def get_image(self, file):
        return api("get_image", {"file": file})

    def can_send_image(self):
        return api("can_send_image")

    def ocr_image(self, image):
        return api("ocr_image", {"image": image})

    # 语音
    def get_record(self, file, out_format):
        return api("get_record", {"file": file, "out_format": out_format})

    def can_send_record(self):
        return api("can_send_record")

    # 处理
    def set_friend_add_request(self, flag, remark, approve=True):
        return api("set_friend_add_request", {"flag": flag, "remark": remark, "approve": approve})

    def set_group_add_request(self, flag, sub_type, reason, approve=True):
        return api("set_group_add_request", {"flag": flag, "sub_type": sub_type, "reason": reason, "approve": approve})

    # 群信息
    def get_group_info(self, group_id, no_cache=False):
        return api("get_group_info", {"group_id": group_id, "no_cache": no_cache})

    def get_group_list(self, no_cache=False):
        return api("get_group_list", {"no_cache": no_cache})

    def get_group_member_info(self, group_id, user_id, no_cache=False):
        return api("get_group_member_info", {"group_id": group_id, "user_id": user_id, "no_cache": no_cache})

    def get_group_member_list(self, group_id, no_cache=False):
        return api("get_group_member_list", {"group_id": group_id, "no_cache": no_cache})

    def get_group_honor_info(self, group_id, type):
        return api("get_group_honor_info", {"group_id": group_id, "type": type})

    def get_group_system_msg(self):
        return api("get_group_system_msg")

    def get_essence_msg_list(self, group_id):
        return api("get_essence_msg_list", {"group_id", group_id})

    def get_group_at_all_remain(self, group_id):
        return api("get_group_at_all_remain", {"group_id", group_id})

    # 群设置
    def set_group_name(self, group_id, group_name):
        return api("set_group_name", {"group_id": group_id, "group_name": group_name})

    def set_group_portrait(self, group_id, file, cache=1):
        return api("set_group_portrait", {"group_id": group_id, "file": file, "cache": cache})

    def set_group_admin(self, group_id, user_id, enable=True):
        return api("set_group_admin", {"group_id": group_id, "user_id": user_id, "enable": enable})

    def set_group_card(self, group_id, user_id, card=""):
        return api("set_group_card", {"group_id": group_id, "user_id": user_id, "card": card})

    def set_group_special_title(self, group_id, user_id, special_title="", duration=-1):
        return api("set_group_special_title",
                   {"group_id": group_id, "user_id": user_id, "special_title": special_title, "duration": duration})

    # 群操作
    def set_group_ban(self, group_id, user_id, duration=30 * 60):
        return api("set_group_ban", {"group_id": group_id, "user_id": user_id, "duration": duration})

    def set_group_whole_ban(self, group_id, enable=True):
        return api("set_group_whole_ban", {"group_id": group_id, "enable": enable})

    def set_group_anonymous_ban(self, group_id, anonymous, duration=30 * 60):
        return api("set_group_anonymous_ban", {"group_id": group_id, "anonymous": anonymous, "duration": duration})

    def set_essence_msg(self, message_id):
        return api("set_essence_msg", {"message_id": message_id})

    def delete_essence_msg(self, message_id):
        return api("delete_essence_msg", {"message_id": message_id})

    def send_group_sign(self, group_id):
        return api("send_group_sign", {"group_id": group_id})

    def set_group_anonymous(self, group_id, enable=True):
        return api("set_group_anonymous", {"group_id": group_id, "enable": enable})

    def _send_group_notice(self, group_id, content, image=None):
        return api("_send_group_notice", {"group_id": group_id, "content": content, "image": image})

    def _get_group_notice(self, group_id):
        return api("_get_group_notice", {"group_id": group_id})

    def set_group_kick(self, group_id, user_id, reject_add_request=False):
        return api("set_group_kick",
                   {"group_id": group_id, "user_id": user_id, "reject_add_request": reject_add_request})

    def set_group_leave(self, group_id, is_dismiss=False):
        return api("set_group_leave", {"group_id": group_id, "is_dismiss": is_dismiss})

    # 文件
    def upload_group_file(self, group_id, file, name, folder):
        return api("upload_group_file", {"group_id": group_id, "file": file, "name": name, "folder": folder})

    def delete_group_file(self, group_id, file_id, busid):
        return api("delete_group_file", {"group_id": group_id, "file_id": file_id, "busid": busid})

    def create_group_file_folder(self, group_id, name, parent_id="/"):
        return api("create_group_file_folder", {"group_id": group_id, "name": name, "parent_id": parent_id})

    def delete_group_folder(self, group_id, folder_id):
        return api("delete_group_folder", {"group_id": group_id, "folder_id": folder_id})

    def get_group_file_system_info(self, group_id):
        return api("get_group_file_system_info", {"group_id": group_id})

    def get_group_root_files(self, group_id):
        return api("get_group_root_files", {"group_id": group_id})

    def get_group_files_by_folder(self, group_id, folder_id):
        return api("get_group_files_by_folder", {"group_id": group_id, "folder_id": folder_id})

    def get_group_file_url(self, group_id, file_id, busid):
        return api("get_group_file_url", {"group_id": group_id, "file_id": file_id, "busid": busid})

    def upload_private_file(self, user_id, file, name):
        return api("upload_private_file", {"user_id": user_id, "file": file, "name": name})

    # Go-Cqhttp相关
    def get_cookies(self, domain):
        return api("get_cookies", {"domain", domain})

    def get_csrf_token(self):
        return api("get_csrf_token")

    def get_credentials(self, domain):
        return api("get_credentials", {"domain": domain})

    def get_version_info(self):
        return api("get_version_info")

    def get_status(self):
        return api("get_status")

    def clean_cache(self):
        return api("clean_cache")

    def reload_event_filter(self, file):
        return api("reload_event_filter", {"file": file})

    def download_file(self, url, thread_count, headers):
        return api("download_file", {"url": url, "thread_count": thread_count, "headers": headers})

    def check_url_safely(self, url):
        return api("check_url_safely", {"url": url})

    # 快速操作
    def handle_quick_operation(self, args):
        return api("handle_quick_operation", args)
