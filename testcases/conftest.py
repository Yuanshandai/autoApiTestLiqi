import pytest
import allure
from common.DB_Handle import mh, rh
from common.Conf_Handle import ih
from common.Request_Handle import RequestsSessionHandle
from common.Logging_Handle import log, err_log
import time
import random


def pytest_sessionfinish(session):
    with open("{}/result/environment.properties".format(session.config.rootdir), "w") as f:
        f.write("browser=chrome\nbackend=staging\ndomain=http://baidu.com")





@allure.story("这是前置操作11111")
@pytest.fixture()
def login():
    print("请输入账号密码")


# 读取conf.ini配置文件中host值
@pytest.fixture()
def get_host():
    # 读conf.ini配置文件获取host
    return ih.get_str("url", option="url")


# 读取conf.ini配置文件中account值
@pytest.fixture()
def get_account():
    # 读conf.ini配置文件获取host
    return ih.get_str("account", option="account")


# 获取当前微秒级时间戳,作为唯一recordId
@pytest.fixture()
def create_recordId():
    return str(round(time.time() * 1000000))


# 生成唯一remark
@pytest.fixture()
def create_remark():
    return "lq" + str(round(time.time() * 1000000))


# 生成学员id : stuWechat
@pytest.fixture()
def create_stuWechat():
    return "wxid_" + str(round(time.time() * 1000000))


# 清除数据库
@pytest.fixture(scope="module")
def delete_data(request):
    yield
    key = request.param
    sql1 = 'DELETE FROM wechat_auto_apply WHERE account = "dongfangyao"'
    sql2 = 'DELETE FROM wechat_heartbeat_history WHERE login_account = "dongfangyao"'
    sql3 = 'DELETE FROM wechat_friend WHERE wechat_id = "wxid_ss245739845"'
    sql4 = 'DELETE FROM wechat_auto_apply_friend_record WHERE wechat_id = "wxid_ss245739845"'
    sql5 = 'SELECT * FROM wechat_auto_apply WHERE account = "dongfangyao" ORDER BY id DESC'
    sql6 = 'SELECT * FROM wechat_heartbeat_history WHERE login_account = "dongfangyao" ORDER BY update_time DESC'
    sql7 = 'SELECT * FROM wechat_friend WHERE wechat_id = "wxid_ss245739845" ORDER BY id DESC'
    sql8 = 'SELECT * FROM wechat_auto_apply_friend_record WHERE wechat_id = "wxid_ss245739845" ORDER BY id DESC'
    mh.execute_sql(sql1)
    mh.execute_sql(sql2)
    mh.execute_sql(sql3)
    mh.execute_sql(sql4)

    # 清空redis中的指令
    # key = Test_add_friend.teacher_wechat + "_{apply_friend_list}"
    # log.info("老师微信是:%s" % Test_add_friend.teacher_wechat)
    log.info(f"key值是:{key}")
    rh.delete(key)
    assert rh.list_getone(key) is None, "redis中存在指令：%s" % rh.list_getone(key)
    # if not mh.find_all(sql5) :
    #     log.info(f"wechat_auto_apply表中存在数据：{mh.find_all(sql5)}")
    assert mh.find_all(sql5) == (), f"wechat_auto_apply表中存在数据：{mh.find_all(sql5)}"
    log.info("wechat_auto_apply表数据已经被清除")
    assert mh.find_all(sql6) == (), f"wechat_heartbeat_history表中存在数据：{mh.find_all(sql6)}"
    log.info("wechat_heartbeat_history表中数据已经被清除")
    assert mh.find_all(sql7) == (), f"wechat_friend表中存在数据：{mh.find_all(sql7)}"
    log.info("wechat_friend表中数据已经被清除")
    assert mh.find_all(sql8) == (), f"wechat_auto_apply_friend_record表中存在数据：{mh.find_all(sql8)}"
    log.info("wechat_auto_apply_friend_record表中数据已经被清除")
