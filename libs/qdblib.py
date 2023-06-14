import os
import base64
class dbError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self)
        self.ErrorInfo=ErrorInfo
    def __str__(self):
        return self.ErrorInfo
class QDB:
    def setpath(self,path):
        self.path=path
    def opendb(self,name):
        self.name=name
    def deldb(self,name=""):
        if not name and self.name:
            os.remove(f"{self.path}/{self.name}.qdb")
        elif name:
            os.remove(f"{self.path}/{name}.qdb")
        else:
            raise dbError("数据桶未指定")
    def read(self,key="*"):
        if self.name:
            if os.listdir(self.path).count(f"{self.name}.qdb")==0:
                with open(f"{self.path}/{self.name}.qdb","w")as f:
                    f.write("")
            with open(f"{self.path}/{self.name}.qdb", "r") as f:
                db = f.read().splitlines()
            if key=="*":
                data=[]
                for i in db:
                    key=str(base64.b64decode(i[:i.find("db0x00")]),"utf-8")
                    value=str(base64.b64decode(i[i.find("db0x00")+6:i.find("db0xFF")]),"utf-8")
                    data.append({key:value})
                return data
            else:
                data = []
                for i in db:
                    if str(base64.b64decode(i[:i.find("db0x00")]), "utf-8")==key:
                        data.append(str(base64.b64decode(i[i.find("db0x00") + 6:i.find("db0xFF")]), "utf-8"))
                return data
        else:
            raise dbError("数据桶未指定")
    def write(self,key,value):
        if self.name:
            if os.listdir(self.path).count(f"{self.name}.qdb")==0:
                with open(f"{self.path}/{self.name}.qdb","w")as f:
                    f.write("")
            with open(f"{self.path}/{self.name}.qdb", "r") as r:
                r.seek(len(r.read()))
            with open(f"{self.path}/{self.name}.qdb","a")as f:
                f.write("%sdb0x00%sdb0xFF\n"%(str(base64.b64encode(str(key).encode("utf-8")),"utf-8"),str(base64.b64encode(str(value).encode("utf-8")),"utf-8")))
        else:
            raise dbError("数据桶未指定")
    def set_one(self,key,value):
        if self.name:
            if os.listdir(self.path).count(f"{self.name}.qdb")==0:
                with open(f"{self.path}/{self.name}.qdb","w")as f:
                    f.write("")
            with open(f"{self.path}/{self.name}.qdb", "r") as f:
                db = f.read().splitlines()
            for tag in range(0,len(db)):
                i=db[tag]
                if str(base64.b64decode(i[:i.find("db0x00")]), "utf-8")==key:
                    db[tag]="%sdb0x00%sdb0xFF"%(i[:i.find("db0x00")],str(base64.b64encode(str(value).encode("utf-8")), "utf-8"))
                    break
            with open(f"{self.path}/{self.name}.qdb", "w") as w:
                w.write("")
            with open(f"{self.path}/{self.name}.qdb", "a") as f:
                for i in range(0,len(db)):
                    db[i]=db[i]+"\n"
                f.writelines(db)
        else:
            raise dbError("数据桶未指定")
    def set(self,key,value):
        if self.name:
            if os.listdir(self.path).count(f"{self.name}.qdb")==0:
                with open(f"{self.path}/{self.name}.qdb","w")as f:
                    f.write("")
            with open(f"{self.path}/{self.name}.qdb", "r") as f:
                db = f.read().splitlines()
            for tag in range(0,len(db)):
                i=db[tag]
                if str(base64.b64decode(i[:i.find("db0x00")]), "utf-8")==key:
                    db[tag]="%sdb0x00%sdb0xFF"%(i[:i.find("db0x00")],str(base64.b64encode(str(value).encode("utf-8")), "utf-8"))
            with open(f"{self.path}/{self.name}.qdb", "w") as w:
                w.write("")
            with open(f"{self.path}/{self.name}.qdb", "a") as f:
                for i in range(0,len(db)):
                    db[i]=db[i]+"\n"
                f.writelines(db)
        else:
            raise dbError("数据桶未指定")
    def del_one(self,key):
        if self.name:
            if os.listdir(self.path).count(f"{self.name}.qdb")==0:
                with open(f"{self.path}/{self.name}.qdb","w")as f:
                    f.write("")
            with open(f"{self.path}/{self.name}.qdb", "r") as f:
                db = f.read().splitlines()
            for tag in range(0,len(db)):
                i=db[tag]
                if str(base64.b64decode(i[:i.find("db0x00")]), "utf-8")==key:
                    db.pop(tag)
                    break
            with open(f"{self.path}/{self.name}.qdb", "w") as w:
                w.write("")
            with open(f"{self.path}/{self.name}.qdb", "a") as f:
                for i in range(0,len(db)):
                    db[i]=db[i]+"\n"
                f.writelines(db)
        else:
            raise dbError("数据桶未指定")
    def delete(self,key):
        if self.name:
            if os.listdir(self.path).count(f"{self.name}.qdb")==0:
                with open(f"{self.path}/{self.name}.qdb","w")as f:
                    f.write("")
            with open(f"{self.path}/{self.name}.qdb", "r") as f:
                db = f.read().splitlines()
                for tag in range(0,len(db)):
                    i=db[tag]
                    if str(base64.b64decode(i[:i.find("db0x00")]), "utf-8")==key:
                        db[tag]=""
            with open(f"{self.path}/{self.name}.qdb", "w") as w:
                w.write("")
            with open(f"{self.path}/{self.name}.qdb", "a") as f:
                for i in range(0,len(db)):
                    if db[i]:
                        db[i]=db[i]+"\n"
                f.writelines(db)
        else:
            raise dbError("数据桶未指定")