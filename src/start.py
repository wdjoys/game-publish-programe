# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 13:41:07
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-07 14:30:52


from multiprocessing import Process

from web.main import run as api_run
from crawler.main import run as crawler_run


if __name__ == "__main__":

    # 需要单独进程运行的函数列表
    target_func_list = [api_run, crawler_run]
    # 进程列表
    process_list = []

    for target_func in target_func_list:
        # 创建进程
        process = Process(target=target_func)
        # 进程启动
        process.start()
        # 进程添加到进程列表
        process_list.append(process)

    # 主线程等待分线程程序执行完毕再退出
    [process.join() for process in process_list]
