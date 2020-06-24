# -*-coding:utf-8 -*-
import pytest
import allure
from common.Conf_Handle import ih
from common.Request_Handle import myRequest
from common.Logging_Handle import log, err_log
from common.DB_Handle import mh, rh
import time


@allure.feature("测试自动加好友并同意,数据入库")
class Test_add_friend(object):
    # 创建RequestsSessionHandle对象
    #myRequest = RequestsSessionHandle()
    # # 读conf.ini配置文件获取host
    # host = ih.get_str("url", option="url")
    host = ""
    account = ""
    recordId = ""
    remark = ""
    stuWechat = ""
    teacher_wechat = ""
    operationId = ""
    operationType = ""
    key = ""

    @allure.story("自动加好友")
    @allure.title("测试自动加好友pushAutoApply接口")
    @allure.description("用例描述：1.验证自动加好友接口返回值")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第一步：发送加好友请求")
    @pytest.mark.run(order=1)
    # conftest.py文件中get_host函数 读取conf.ini文件中url，存储在类变量host中
    def test_send_addFriendRequest(self, get_host, get_account, create_recordId, create_remark, create_stuWechat):
        """
        推加好友指令
        :param get_host:
        :param get_account:
        :param create_recordId:
        :param create_remark:
        :param create_stuWechat:
        :return:
        """
        # 读取host
        Test_add_friend.host = get_host
        # 读取accout
        Test_add_friend.account = get_account
        # 得到加好友路径
        self.addFriendUrl = ih.get_str("url", option="addFriendUrl")
        # 拼接完整url
        url = Test_add_friend.host + self.addFriendUrl
        log.info(f"加好友接口的地址是:{url}")
        # 获取recordID
        Test_add_friend.recordId = create_recordId
        # 写进conf.ini配置文件,发小程序时使用
        ih.write_data("recordId","recordId",Test_add_friend.recordId)
        # 获取remark(不能重复)
        Test_add_friend.remark = create_remark
        # 写进conf.ini配置文件,发小程序时使用
        ih.write_data("remark", "remark", Test_add_friend.remark)
        # 获取stuWechat
        Test_add_friend.stuWechat = create_stuWechat
        # 写进conf.ini配置文件,发小程序时使用
        ih.write_data("stuWechat","stuWechat",Test_add_friend.stuWechat)
        # 读取teacher_wechat
        Test_add_friend.teacher_wechat = ih.get_str("teacher_wechat", option="teacher_wechat")

        data = {
            "operationType": 33,
            "paramList": [
                {
                    "account": Test_add_friend.account,
                    "accountWechat": Test_add_friend.teacher_wechat,
                    "additionalInfo": "附加信息",
                    "applyPatternContent": "同意一下",
                    "priority": 0,
                    "recordId": Test_add_friend.recordId,
                    "remark": Test_add_friend.remark,
                    "stuWechat": Test_add_friend.stuWechat,
                    "notNeedCover": "1"
                }
            ],
            "source": "skynet"
        }

        log.info(f"加好友接口的入参是：{data}")
        log.info("开始发送加好友请求")
        response = myRequest.send(url=url, method="post", json=data)
        log.info(f"============接口响应结果：{response.json()}")
        # 将返回结果转成字典形式
        result = response.json()
        log.info(f"状态码的值是: {response.status_code}")
        # 判断状态码=200
        assert (response.status_code == 200), "判断状态码:response.status_code:%s 等于200" % response.status_code
        log.info("===状态码正确======")
        log.info("flag的值是: {flag}".format(flag=result["flag"]))
        # 判断flag是1
        assert (int(result["flag"]) == 1), "判断flag:%s 等于1" % result["flag"]

        # 判断flag如果是0，打出具体的错误信息message
        if int(result["flag"]) == 0:
            err_log.error(r"------出现错误：message:{message}".format(message=result["message"]))

    @allure.story("自动加好友")
    @allure.title("测试redis中存在加好友指令")
    @allure.description("描述：验证redis中存在刚刚放入的加好友指令")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第二步：验证数据库")
    @pytest.mark.run(order=2)
    def test_redis(self):
        Test_add_friend.key = Test_add_friend.teacher_wechat + "_{apply_friend_list}"
        log.info("老师微信是:%s" % Test_add_friend.teacher_wechat)
        log.info(f"key值是:{Test_add_friend.key}")
        result = rh.list_getone(Test_add_friend.key)
        log.info(f"最新放入redis的加好友指令是:{result}")
        assert result["recordId"] == Test_add_friend.recordId, "判断redis中最右侧的指令的recordId是:%s" % result["recordId"]
        log.info("redis中最新一条指令的recordId是：%s" % result["recordId"])
        log.info("生成的recordId是：%s" % Test_add_friend.recordId)
        log.info("redis中存在刚放入的加好友指令")

    @allure.story("自动加好友")
    @allure.title("测试心跳heartbreat接口")
    @allure.description("用例描述：3.验证心跳接口")
    @allure.severity("blocker")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第三步：心跳")
    @pytest.mark.run(order=3)
    def test_heartbeat(self):
        """
        请求心跳接口取指令
        :return:
        """
        # 得到心跳接口路径
        self.heartbeat = ih.get_str("url", option="heartbeat")
        # 拼接完整url
        url = Test_add_friend.host + self.heartbeat
        log.info(f"心跳接口接口的地址是:{url}")
        data = {
            "account": Test_add_friend.account,
            "canReceiveNewOrder": True,
            "isRoot": True,
            "laterReceive": False,
            "miPushId": "PFHBfYNju2pJ7970mm3OvnSiUgFIC\/d7wTctDTfP+3n5RXTnRn0Eyqes2yJaVzQm",
            "os": "android",
            "otherWechatIds": ["wxid_y2twb3cy6a3o22_YC"],
            "version": "3.1.9",
            "wechatDeviceId": "11ea23e764c1302a",
            "wechatId": Test_add_friend.teacher_wechat,
            "wechatLive": True,
            "wechatVersion": "7.0.4",
            "wxBackgroundMode": True,
            "wxHackEnabled": True,
            "versionName": "3.0.6.1",
            "versionCode": "69",
            "wechatAccount": Test_add_friend.teacher_wechat,
            "wechatVersionCode": "1420",
            "source": "app_root",
            "loginAccount": Test_add_friend.account,
            "phoneDeviceId": "11ea23e764c1302a"
        }
        log.info(f"心跳接口的入参是：{data}")
        log.info("=====开始请求心跳接口")
        response = myRequest.send(url=url, method="post", json=data)
        log.info(f"============接口响应结果：{response.json()}")
        # 将返回结果转成字典形式
        result = response.json()
        log.info(f"状态码的值是: {response.status_code}")
        # 判断状态码=200
        assert (response.status_code == 200), "判断状态码:response.status_code:%s 等于200" % response.status_code
        log.info("===状态码正确======")
        log.info("operationId的值是: {operationId}".format(operationId=result["data"]["operationId"]))
        log.info(type(result["data"]))
        # 判断operationId是1
        assert (int(result["data"]["operationId"]) != -1), "判断operationId:%s 不等于-1" % result["data"]["operationId"]
        # 得到心跳接口的operationId
        Test_add_friend.operationId = result["data"]["operationId"]
        # 得到心跳接口的operationType
        Test_add_friend.operationType = result["data"]["operationType"]
        # 得到心跳接口的recordId
        Test_add_friend.recordId = result["data"]["recordId"]
        # 判断operationId如果是-1，打出具体的错误信息message
        if int(result["data"]["operationId"]) == -1:
            err_log.error(r"------出现错误：心跳接口没有取到指令")
        return result["data"]["operationId"]

    @allure.story("自动加好友")
    @allure.title("测试加好友指令入库")
    @allure.description("描述：4.验证加好友指令入库")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第四步：验证数据库中存在加好友指令")
    @pytest.mark.run(order=4)
    def test_mysql_wechat_auto_apply(self):
        if Test_add_friend.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证数据入库操作 标记失败")
        sql = 'SELECT * FROM wechat_auto_apply WHERE account = "dongfangyao" ORDER BY id DESC '
        result = mh.find_one(sql)
        log.info(f"数据库中account=’dongfangyao‘的最新一条加好友数据是{result}")
        log.info(f"数据库中recordId是{result[1]}")
        log.info(f"插入的recordId是{Test_add_friend.recordId}")
        assert result[1] == Test_add_friend.recordId, "最近一条数据的recordId是%s" % Test_add_friend.recordId
        assert int(result[7]) == -1, "state字段是：%s" % result[7]
        log.info("数据库中存在正确的加好友指令")

    @allure.story("自动加好友")
    @allure.title("测试operationCallback接口")
    @allure.description("用例描述：5.operationCallback 具体干啥的不知道")
    @allure.severity("blocker")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第五步：operationCallback")
    @pytest.mark.run(order=5)
    def test_operationCallback(self):
        if Test_add_friend.operationId == "":
            log.error("心跳接口又没有取到指令。。。。。。。")
            pytest.xfail(reason="心跳接口没有取到指令，operationCallback接口标记失败")
        # 得到operationCallback接口路径
        self.operationCallback = ih.get_str("url", option="operationCallback")
        # 拼接完整url
        url = Test_add_friend.host + self.operationCallback
        log.info(f"operationCallback接口的地址是:{url}")
        data = {
            "desc": "轮询到自动操作指令operationId:286 operationType:41 hasNewVersionfalse",
            "operationId": Test_add_friend.operationId,
            "operationType": Test_add_friend.operationType,
            "state": -2,
            "wechatId": Test_add_friend.teacher_wechat,
            "versionName": "3.1.13",
            "versionCode": "97",
            "wechatAccount": Test_add_friend.teacher_wechat,
            "wechatVersion": "7.0.5",
            "wechatVersionCode": "1440",
            "source": "app_root",
            "loginAccount": "${account}",
            "phoneDeviceId": "2cd6f7c3b0a15b2f",
            "channel": "platform"
        }
        log.info(f"operationCallback接口的入参是：{data}")
        log.info("=====开始请求operationCallback接口")
        response = myRequest.send(url=url, method="post", json=data)
        log.info(f"============接口响应结果：{response.json()}")
        # 将返回结果转成字典形式
        result = response.json()
        log.info(f"状态码的值是: {response.status_code}")
        # 判断状态码=200
        assert (response.status_code == 200), "判断状态码:response.status_code:%s 等于200" % response.status_code
        log.info("===状态码正确======")
        # 判断flag是1
        assert (int(result["flag"]) == 1), "判断flag:%s 等于1" % result["flag"]

        # 判断flag如果是0，打出具体的错误信息message
        if int(result["flag"]) == 0:
            err_log.error(r"------出现错误：message:{message}".format(message=result["message"]))

    @allure.story("自动加好友")
    @allure.title("测试加好友指令入库")
    @allure.description("描述：验证数据库中加好友指令是status=-2")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第六步：验证数据库中加好友指令是status=-2")
    @pytest.mark.run(order=6)
    def test_mysql_wechat_auto_apply1(self):
        if Test_add_friend.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证数据是否入库操作 标记失败")
        sql = 'SELECT * FROM wechat_auto_apply WHERE account = "dongfangyao" ORDER BY id DESC '
        result = mh.find_one(sql)
        log.info(f"数据库中account=’dongfangyao‘的最新一条加好友数据是{result}")
        log.info(f"数据库中recordId是{result[1]}")
        log.info(f"插入的recordId是{Test_add_friend.recordId}")
        assert result[1] == Test_add_friend.recordId, "最近一条数据的recordId是%s" % Test_add_friend.recordId
        assert int(result[7]) == -2, "state字段是：%s" % result[7]
        log.info("数据库中state值正确")

    @allure.story("自动加好友")
    @allure.title("测试operationCallback接口")
    @allure.description("用例描述：4.operationCallback 还是这个接口呵呵呵呵")
    @allure.severity("blocker")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第七步：operationCallback")
    @pytest.mark.run(order=7)
    def test_operationCallback1(self):
        if Test_add_friend.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，operationCallback接口标记失败")
        # 得到operationCallback接口路径
        self.operationCallback = ih.get_str("url", option="operationCallback")
        # 拼接完整url
        url = Test_add_friend.host + self.operationCallback
        log.info(f"operationCallback接口的地址是:{url}")
        data = {
            "additionalInfo": "additionalInfo1",
            "operationId": Test_add_friend.operationId,
            "operationType": Test_add_friend.operationType,
            "recordId": Test_add_friend.recordId,
            "state": 0,
            "system": "lsxtest",
            "wechatId": Test_add_friend.teacher_wechat,
            "versionName": "3.1.13",
            "versionCode": "97",
            "wechatAccount": Test_add_friend.teacher_wechat,
            "wechatVersion": "7.0.5",
            "wechatVersionCode": "1440",
            "source": "app_root",
            "loginAccount": Test_add_friend.account,
            "phoneDeviceId": "2cd6f7c3b0a15b2f",
            "channel": "platform"
        }
        log.info(f"operationCallback1接口的入参是：{data}")
        log.info("=====开始请求operationCallback1接口")
        response = myRequest.send(url=url, method="post", json=data)
        log.info(f"============接口响应结果：{response.json()}")
        # 将返回结果转成字典形式
        result = response.json()
        log.info(f"状态码的值是: {response.status_code}")
        # 判断状态码=200
        assert (response.status_code == 200), "判断状态码:response.status_code:%s 等于200" % response.status_code
        log.info("===状态码正确======")
        # 判断flag是1
        assert (int(result["flag"]) == 1), "判断flag:%s 等于1" % result["flag"]

        # 判断flag如果是0，打出具体的错误信息message
        if int(result["flag"]) == 0:
            err_log.error(r"------出现错误：message:{message}".format(message=result["message"]))

    @allure.story("自动加好友")
    @allure.title("测试加好友指令入库")
    @allure.description("描述：验证数据库中加好友指令是status=-2")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第四步：验证数据库中加好友指令是status=0")
    @pytest.mark.run(order=8)
    def test_mysql_wechat_auto_apply2(self):
        if Test_add_friend.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证status操作标记失败")
        sql = 'SELECT * FROM wechat_auto_apply WHERE account = "dongfangyao" ORDER BY id DESC '
        result = mh.find_one(sql)
        log.info(f"wechat_auto_apply表中account=’dongfangyao‘的最新一条加好友数据是{result}")
        log.info(f"wechat_auto_apply表中recordId是{result[1]}")
        log.info(f"插入的recordId是{Test_add_friend.recordId}")
        assert result[1] == Test_add_friend.recordId, "最近一条数据的recordId是%s" % Test_add_friend.recordId
        assert int(result[7]) == 0, "state字段是：%s" % result[7]
        log.info("wechat_auto_apply表中state值正确")

    @allure.story("自动加好友")
    @allure.title("测试uploadWxFriends接口")
    @allure.description("用例描述：9.uploadWxFriends 还是这个接口呵呵呵呵")
    @allure.severity("blocker")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第五步：uploadWxFriends")
    @pytest.mark.run(order=9)
    def test_uploadWxFriends(self):
        """
        通讯录上报接口
        :return:
        """
        if Test_add_friend.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，operationCallback接口标记失败")
        # 得到operationCallback接口路径
        self.uploadWxFriends = ih.get_str("url", option="uploadWxFriends")
        # 拼接完整url
        url = Test_add_friend.host + self.uploadWxFriends
        log.info(f"uploadWxFriends接口的地址是:{url}")
        data = {
            "state": "add",
            "wechatFriendsList": [{
                "nsAliasName": Test_add_friend.stuWechat,
                "nsCity": "荆州",
                "nsRemark": Test_add_friend.remark,
                "nsRemarkPYFull": "",
                "nsRemarkPYShort": "",
                "nsEncodeUserName": "v1_e1a7013e58d94347d9e984b51c9a842a47e578dba1f9aa8ad680fd4e712829c7@stranger",
                "nsHeadHDImgUrl": "http:\/\/wx.qlogo.cn\/mmhead\/ver_1\/4BKSYQKotBqf8ZjqmctFeR6LHia9FMaGIfkDoIT5wyHn9Z1ICfrPdeTZfXZDnT4ic30XZoyO4xlpWIQRyLkMUJdQ\/0",
                "nsHeadImgUrl": "http:\/\/wx.qlogo.cn\/mmhead\/ver_1"
                                "\/4BKSYQKotBqf8ZjqmctFeR6LHia9FMaGIfkDoIT5wyHn9Z1ICfrPdeTZfXZDnT4ic30XZoyO4xlpWIQRyLkMUJdQ\/96",
                "nsNickName": "梦迪",
                "nsProvince": "湖北",
                "nsShortPY": "QQ842378405",
                "nsFullPY": "qq842378405",
                "searchString": Test_add_friend.stuWechat,
                "uiSex": 2,
                "nsSignature": "无所畏惧",
                "uiType": 3,
                "nsUsrName": Test_add_friend.stuWechat
            }],
            "wechatId": Test_add_friend.teacher_wechat,
            "versionName": "3.1.13",
            "versionCode": "97",
            "wechatAccount": Test_add_friend.teacher_wechat,
            "wechatVersion": "7.0.5",
            "wechatVersionCode": "1440",
            "source": "app_root",
            "loginAccount": Test_add_friend.account,
            "phoneDeviceId": "2cd6f7c3b0a15b2f",
            "channel": "platform"
        }
        log.info(f"uploadWxFriends接口的入参是：{data}")
        log.info("=====开始请求uploadWxFriends接口")
        response = myRequest.send(url=url, method="post", json=data)
        log.info(f"============接口响应结果：{response.json()}")
        # 将返回结果转成字典形式
        result = response.json()
        log.info(f"状态码的值是: {response.status_code}")
        # 判断状态码=200
        assert (response.status_code == 200), "判断状态码:response.status_code:%s 等于200" % response.status_code
        log.info("===状态码正确======")
        # 判断flag是1
        assert (int(result["flag"]) == 1), "判断flag:%s 等于1" % result["flag"]

        # 判断flag如果是0，打出具体的错误信息message
        if int(result["flag"]) == 0:
            err_log.error(r"------出现错误：message:{message}".format(message=result["message"]))

    @allure.story("自动加好友")
    @allure.title("测试wechat_friend")
    @allure.description("描述：验证wechat_friend表中插入数据")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第四步：验证数据库中wechat_friend表中插入数据")
    @pytest.mark.run(order=10)
    def test_mysql_wechat_friend(self):
        if Test_add_friend.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证数据是否入库操作口标记失败")
        sql = 'SELECT * FROM wechat_friend WHERE wechat_id = "wxid_ss245739845" ORDER BY id DESC'
        result = mh.find_one(sql)
        log.info(f"数据库中account=’dongfangyao‘的最新一条加好友数据是{result}")
        log.info(f"数据库中ns_usr_name是{result[2]}")
        log.info(f"插入的ns_usr_name是{Test_add_friend.stuWechat}")
        assert result[2] == Test_add_friend.stuWechat, "最近一条数据的ns_usr_name是%s" % Test_add_friend.stuWechat
        log.info("wechat_friend表中插入数据正确")


    @allure.story("自动加好友")
    @allure.title("测试wechat_auto_apply_friend_record表中数据")
    @allure.description("描述：验证数据库中加好友指令是status=-2")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第四步：验证数据库中wechat_auto_apply_friend_record表中插入数据")
    @pytest.mark.run(order=11)
    def test_mysql_wechat_auto_apply_friend_record(self):
        if Test_add_friend.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证数据是否入库操作标记失败")
        time.sleep(2)
        sql = 'SELECT * FROM wechat_auto_apply_friend_record ' \
              'WHERE wechat_id = "wxid_ss245739845" ORDER BY id DESC limit 1'

        result = mh.find_one(sql)
        log.info(f"wechat_auto_apply_friend_record表中account=’dongfangyao‘的最新一条数据是{result}")
        log.info(f"wechat_auto_apply_friend_record表中ns_usr_name是{result[2]}")
        log.info(f"插入的ns_usr_name是{Test_add_friend.stuWechat}")
        assert result[2] == Test_add_friend.stuWechat, "最近一条数据的ns_usr_name是%s" % Test_add_friend.stuWechat
        log.info("wechat_auto_apply_friend_record表中插入数据正确")

    # @allure.story("自动加好友")
    # @allure.title("删除redis和数据库表中数据")
    # @allure.description("描述：删除数据")
    # @allure.severity("block")
    # @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    # @allure.issue("https://baidu.com", name="这是bug连接")
    # @allure.step("第四步：验证数据库中wechat_auto_apply_friend_record表中插入数据")
    # @pytest.mark.run(order=12)
    # def test_delete_data(self):
    #     sql1 = 'DELETE FROM wechat_auto_apply WHERE account = "dongfangyao"'
    #     sql2 = 'DELETE FROM wechat_heartbeat_history WHERE login_account = "dongfangyao"'
    #     sql3 = 'DELETE FROM wechat_friend WHERE wechat_id = "wxid_ss245739845"'
    #     sql4 = 'DELETE FROM wechat_auto_apply_friend_record WHERE wechat_id = "wxid_ss245739845"'
    #     sql5 = 'SELECT * FROM wechat_auto_apply WHERE account = "dongfangyao" ORDER BY id DESC'
    #     sql6 = 'SELECT * FROM wechat_heartbeat_history WHERE login_account = "dongfangyao" ORDER BY update_time DESC'
    #     sql7 = 'SELECT * FROM wechat_friend WHERE wechat_id = "wxid_ss245739845" ORDER BY id DESC'
    #     sql8 = 'SELECT * FROM wechat_auto_apply_friend_record WHERE wechat_id = "wxid_ss245739845" ORDER BY id DESC'
    #     mh.execute_sql(sql1)
    #     mh.execute_sql(sql2)
    #     mh.execute_sql(sql3)
    #     mh.execute_sql(sql4)
    #
    #     # 清空redis中的指令
    #     key = Test_add_friend.teacher_wechat + "_{apply_friend_list}"
    #     log.info("老师微信是:%s" % Test_add_friend.teacher_wechat)
    #     log.info(f"key值是:{key}")
    #     rh.delete(key)
    #     assert rh.list_getone(key) is None, "redis中存在指令：%s" % rh.list_getone(key)
    #     # if not mh.find_all(sql5) :
    #     #     log.info(f"wechat_auto_apply表中存在数据：{mh.find_all(sql5)}")
    #     assert mh.find_all(sql5) == (), f"wechat_auto_apply表中存在数据：{mh.find_all(sql5)}"
    #     log.info("wechat_auto_apply表数据已经被清除")
    #     assert mh.find_all(sql6) == (), f"wechat_heartbeat_history表中存在数据：{mh.find_all(sql6)}"
    #     log.info("wechat_heartbeat_history表中数据已经被清除")
    #     assert mh.find_all(sql7) == (), f"wechat_friend表中存在数据：{mh.find_all(sql7)}"
    #     log.info("wechat_friend表中数据已经被清除")
    #     assert mh.find_all(sql8) == (), f"wechat_auto_apply_friend_record表中存在数据：{mh.find_all(sql8)}"
    #     log.info("wechat_auto_apply_friend_record表中数据已经被清除")


if __name__ == "__main__":
    pytest.main(["-s", "Test_case1_add_friend.py"])
