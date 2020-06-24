import os

BASEDIR = os.path.dirname(os.path.dirname(__file__))
print(os.path.dirname(__file__))
print(BASEDIR)

# 配置文件存放路径
CONF_DIR = os.path.join(BASEDIR, "conf")

# 数据存放路径
DATA_DIR = os.path.join(BASEDIR, "data")

# 日志存放路径
LOGS_DIR = os.path.join(BASEDIR, "logs")

# 测试报告存放路径
REPORTS_DIR = os.path.join(BASEDIR, "reports")

# Allure测试报告存放路径
ALLURE_DIR = os.path.join(REPORTS_DIR, "allure")

# AllurePlus(在allure测试报告基础上升级的测试报告，查看更加简单)测试报告存放路径
ALLURE_PLUS_DIR = os.path.join(REPORTS_DIR, "allure-plus")


print(ALLURE_PLUS_DIR)
print(ALLURE_DIR)
