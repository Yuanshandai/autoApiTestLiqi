__author__ = 'liqi'
__time__ = '2020/6/2'
"""
封装log方法
"""
import logging
import os
import time

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'waring': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}
# 创建logger
logger = logging.getLogger()
level = 'default'


# 创建日志文件
def create_file(filename):
    # 得到路径
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        # 打开一个文件只用于写入。如果该文件已存在则将其覆盖。
        # 如果该文件不存在，创建新文件。
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass


# 给logger添加handler
def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)
    logger.addHandler(MyLog.console)


def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)
    logger.removeHandler(MyLog.console)


def get_current_time():
    return time.strftime(MyLog.date, time.localtime(time.time()))


class MyLog:
    # path得到auto_api_test_liqi 项目所在路径
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = path + '/Log/log.log'
    err_file = path + '/Log/err.log'
    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S'
    # 将日志输出到屏幕
    # 创建handler,用于输出到控制台
    console = logging.StreamHandler()
    # 指定被处理的信息级别，低于lel级别的信息将被忽略
    console.setLevel(LEVELS.get(level, logging.NOTSET))
    # 将日志输出到文件
    # 指定被处理的信息级别，低于lel级别的信息将被忽略
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    # 创建handler用于输出到文件
    handler = logging.FileHandler(log_file, encoding='utf-8')
    err_handler = logging.FileHandler(err_file, encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logger.debug("[DEBUG " + get_current_time() + "]" + log_meg)
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info("[INFO " + get_current_time() + "]" + log_meg)
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning("[WARNING " + get_current_time() + "]" + log_meg)
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logger.error("[ERROR " + get_current_time() + "]" + log_meg)
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.error("[CRITICAL " + get_current_time() + "]" + log_meg)
        remove_handler('critical')


if __name__ == "__main__":
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error")
    MyLog.critical("This is critical message")


