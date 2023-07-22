import os
# 递归删除文件
def delpath(path):
    if os.path.isdir(path):  # 判断是不是文件夹
        for file in os.listdir(path):  # 遍历文件夹里面所有的信息返回到列表中
            delpath(os.path.join(path, file))  # 是文件夹递归自己
        if os.path.exists(path):  # 判断文件夹为空
            os.rmdir(path)  # 删除文件夹

    else:
        if os.path.isfile(path):  # 严谨判断是不是文件
            os.remove(path)  # 删除文件