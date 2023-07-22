import zipfile
import os
def zip(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    dirlist=os.walk(dirpath)
    for path, dirnames, filenames in dirlist:
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        if not path=="./backups":
            if dirnames.count("backups"):
                dirnames.remove("backups")
            fpath = path.replace(dirpath, '')
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))


    zip.close()
