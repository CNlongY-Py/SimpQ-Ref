import _thread


def create(name, data=()):  # 线程创建器
    return _thread.start_new_thread(name, data)
