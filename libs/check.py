import os
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.formatted_text import HTML


def Check():
    if not os.listdir("./config/bot").count(".UNLOCKED"):
        message_dialog(
            title=HTML('<style fg="ansired">Warning</style>'),
            text='此版本为未经允许的SimpQ-DEV版本\n按下ENTER退出').run()
        exit(1)
def serv_lock():
    if os.listdir("./config/bot").count("SERV_UNLOCK"):
        return True