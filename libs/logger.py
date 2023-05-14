import time


def prlog(text):
    with open("./logs/%s.log" % time.strftime("%Y-%m-%d", time.localtime()), "a", encoding="utf-8") as f:
        f.write("%s\n" % text)


class Logger:
    def __init__(self, name, level, buffer):
        self.name = name
        self.formatp = "[%s]" % time.strftime("%Y-%m-%d-%X", time.localtime())
        self.level = level
        self.buffer = buffer

    def error(self, *args):
        txt = ""
        if self.level <= 4:
            for i in args:
                txt += "%s " % i
            self.buffer.insert_text(f"{self.formatp}[ERROR]<{self.name}>:{txt}\n")
            prlog(f"{self.formatp}[ERROR]<{self.name}>:{txt}")

    def warning(self, *args):
        txt = ""
        if self.level <= 3:
            for i in args:
                txt += "%s " % i
            self.buffer.insert_text(f"{self.formatp}[WARNING]<{self.name}>:{txt}\n")
            prlog(f"{self.formatp}[WARNING]<{self.name}>:{txt}")

    def info(self, *args):
        txt = ""
        if self.level <= 2:
            for i in args:
                txt += "%s " % i
            self.buffer.insert_text(f"{self.formatp}[INFO]<{self.name}>:{txt}\n")
            prlog(f"{self.formatp}[INFO]<{self.name}>:{txt}")

    def debug(self, *args):
        txt = ""
        if self.level <= 1:
            for i in args:
                txt += "%s " % i
            self.buffer.insert_text(f"{self.formatp}[DEBUG]<{self.name}>:{txt}\n")
            prlog(f"{self.formatp}[DEBUG]<{self.name}>:{txt}")
