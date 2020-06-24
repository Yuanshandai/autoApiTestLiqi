# -*-coding:utf-8 -*-
import pytest
import allure
from common.Conf_Handle import ih
from common.Request_Handle import myRequest
from common.Logging_Handle import log, err_log
from common.DB_Handle import mh, rh
import time


@allure.feature("测试推送小程序")
class Test_pushMiniPro(object):
    # 创建RequestsSessionHandle对象
    # myRequest = RequestsSessionHandle()
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

    @allure.story("推送小程序")
    @allure.title("测试推送小程序pushAutoApply接口")
    @allure.description("用例描述：1.验证推送小程序接口返回值")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第一步：发送推送小程序请求")
    @pytest.mark.run(order=1)
    @pytest.allure.attach("测试","测试")
    def test_send_pushMiniPro(self, get_host, get_account, create_recordId):
        """
        推推送小程序指令
        :param get_host:
        :param get_account:
        :param create_recordId:
        :param create_remark:
        :param create_stuWechat:
        :return:
        """
        # 读取host
        Test_pushMiniPro.host = get_host
        allure.attach("测试","测试1")
        # 读取accout
        Test_pushMiniPro.account = get_account
        # 得到推送小程序路径
        self.pushMiniProUrl = ih.get_str("url", option="pushMiniPro")
        # 拼接完整url
        url = Test_pushMiniPro.host + self.pushMiniProUrl

        log.info(f"推小程序的接口地址是:{url}")
        # 获取recordID
        Test_pushMiniPro.recordId = create_recordId
        # 获取remark(不能重复)
        # Test_pushMiniPro.remark = create_remark
        # 读conf.ini配置文件获取stuWechat(最近一次推送小程序生成的stuWechat)
        Test_pushMiniPro.stuWechat = ih.get_str("stuWechat", option="stuWechat")
        # 读取teacher_wechat
        Test_pushMiniPro.teacher_wechat = ih.get_str("teacher_wechat", option="teacher_wechat")

        data = {
            "operationType": 36,
            "paramList": [
                {
                    "account": Test_pushMiniPro.account,
                    "accountWechat": Test_pushMiniPro.teacher_wechat,
                    "addParams": {
                        "additionalProp1": "",
                        "additionalProp2": "",
                        "additionalProp3": ""
                    },
                    "additionalInfo": "高意向学员",
                    "guideSpeech": "同学你好",
                    "miniproType": 0,
                    "pictureImg": "string",
                    "pictureTitle": "小程序",
                    "programId": "ws123",
                    "programURL": "http:hh123.com",
                    "recordId": Test_pushMiniPro.recordId,
                    "stuWechat": Test_pushMiniPro.stuWechat,
                    "isFirstPriority": "0",
                    "notNeedCover": "1",
                    "notEnterCommonQueue": "false"
                }
            ],
            "source": "WE"
        }

        log.info(f"推小程序接口的入参是：{data}")
        log.info("开始发送推送小程序请求")
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

    @allure.story("推送小程序")
    @allure.title("测试redis中存在推送小程序指令")
    @allure.description("描述：验证redis中存在刚刚放入的推送小程序指令")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第二步：验证数据库")
    @pytest.mark.run(order=2)
    def test_redis(self):
        Test_pushMiniPro.key = Test_pushMiniPro.teacher_wechat + ih.get_str("postfix", option="pushminipro")
        log.info("老师微信是:%s" % Test_pushMiniPro.teacher_wechat)
        log.info(f"key值是:{Test_pushMiniPro.key}")
        result = rh.list_getone(Test_pushMiniPro.key,0,0)
        assert result is not None, f"result的值是{result},队列里没有推小程序指令"
        log.info(f"最新放入redis的推小程序指令是:{result}")
        assert result["recordId"] == Test_pushMiniPro.recordId, "判断redis中最右侧的指令的recordId是:%s" % result["recordId"]
        log.info("redis中最新一条指令的recordId是：%s" % result["recordId"])
        log.info("生成的recordId是：%s" % Test_pushMiniPro.recordId)
        log.info("redis中存在刚放入的推小程序指令")

    @allure.story("推送小程序")
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
        url = Test_pushMiniPro.host + self.heartbeat
        log.info(f"心跳接口接口的地址是:{url}")
        data = {
            "account": Test_pushMiniPro.account,
            "canReceiveNewOrder": True,
            "isRoot": True,
            "laterReceive": False,
            "miPushId": "PFHBfYNju2pJ7970mm3OvnSiUgFIC\/d7wTctDTfP+3n5RXTnRn0Eyqes2yJaVzQm",
            "os": "android",
            "otherWechatIds": ["wxid_y2twb3cy6a3o22_YC"],
            "version": "3.1.9",
            "wechatDeviceId": "11ea23e764c1302a",
            "wechatId": Test_pushMiniPro.teacher_wechat,
            "wechatLive": True,
            "wechatVersion": "7.0.4",
            "wxBackgroundMode": True,
            "wxHackEnabled": True,
            "versionName": "3.0.6.1",
            "versionCode": "69",
            "wechatAccount": Test_pushMiniPro.teacher_wechat,
            "wechatVersionCode": "1420",
            "source": "app_root",
            "loginAccount": Test_pushMiniPro.account,
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
        Test_pushMiniPro.operationId = result["data"]["operationId"]
        # 得到心跳接口的operationType
        Test_pushMiniPro.operationType = result["data"]["operationType"]
        # 得到心跳接口的recordId
        Test_pushMiniPro.recordId = result["data"]["recordId"]
        # 判断operationId如果是-1，打出具体的错误信息message
        if int(result["data"]["operationId"]) == -1:
            err_log.error(r"------出现错误：心跳接口没有取到指令")
        return result["data"]["operationId"]

    @allure.story("推送小程序")
    @allure.title("测试小程序指令入库")
    @allure.description("描述：4.验证推送小程序指令入库")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第四步：验证数据库中存在推送小程序指令")
    @pytest.mark.run(order=4)
    def test_mysql_wechat_push_minipro(self):
        if Test_pushMiniPro.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证数据入库操作 标记失败")
        sql = 'SELECT * FROM wechat_push_minipro WHERE account = "dongfangyao" ORDER BY id DESC '
        result = mh.find_one(sql)
        log.info(f"wechat_push_minipro表中account=’dongfangyao‘的最新一条推送小程序数据是{result}")
        log.info(f"wechat_push_minipro表中recordId是{result[1]}")
        log.info(f"插入的recordId是{Test_pushMiniPro.recordId}")
        assert result[1] == Test_pushMiniPro.recordId, "最近一条数据的recordId是%s" % Test_pushMiniPro.recordId
        assert int(result[6]) == -1, "state字段是：%s" % result[7]
        log.info("数据库wechat_push_minipro表中存在正确的推送小程序指令")

    @allure.story("推送小程序")
    @allure.title("测试operationCallback接口")
    @allure.description("用例描述：5.operationCallback 具体干啥的不知道")
    @allure.severity("blocker")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第五步：operationCallback")
    @pytest.mark.run(order=5)
    def test_operationCallback(self):
        if Test_pushMiniPro.operationId == "":
            log.error("心跳接口又没有取到指令。。。。。。。")
            pytest.xfail(reason="心跳接口没有取到指令，operationCallback接口标记失败")
        # 得到operationCallback接口路径
        self.operationCallback = ih.get_str("url", option="operationCallback")
        # 拼接完整url
        url = Test_pushMiniPro.host + self.operationCallback
        log.info(f"operationCallback接口的地址是:{url}")
        data = {
            "desc": "轮询到自动操作指令operationId:286 operationType:41 hasNewVersionfalse",
            "operationId": Test_pushMiniPro.operationId,
            "operationType": Test_pushMiniPro.operationType,
            "state": -2,
            "wechatId": Test_pushMiniPro.teacher_wechat,
            "versionName": "3.1.13",
            "versionCode": "97",
            "wechatAccount": Test_pushMiniPro.teacher_wechat,
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

    @allure.story("推送小程序")
    @allure.title("测试推送小程序指令入库")
    @allure.description("描述：验证数据库中推送小程序指令status=-2")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第六步：验证数据库中推送小程序指令是status=-2")
    @pytest.mark.run(order=6)
    def test_mysql_wechat_push_minipro1(self):
        if Test_pushMiniPro.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证数据是否入库操作 标记失败")
        sql = 'SELECT * FROM wechat_push_minipro WHERE account = "dongfangyao" ORDER BY id DESC '
        result = mh.find_one(sql)
        log.info(f"数据库中account=’dongfangyao‘的最新一条推送小程序数据是{result}")
        log.info(f"数据库中recordId是{result[1]}")
        log.info(f"插入的recordId是{Test_pushMiniPro.recordId}")
        assert result[1] == Test_pushMiniPro.recordId, "最近一条数据的recordId是%s" % Test_pushMiniPro.recordId
        assert int(result[6]) == -2, "state字段是：%s" % result[7]
        log.info("数据库中state值正确")

    @allure.story("推送小程序")
    @allure.title("测试operationCallback接口")
    @allure.description("用例描述：4.operationCallback 还是这个接口呵呵呵呵")
    @allure.severity("blocker")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第七步：operationCallback")
    @pytest.mark.run(order=7)
    def test_operationCallback1(self):
        if Test_pushMiniPro.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，operationCallback接口标记失败")
        # 得到operationCallback接口路径
        self.operationCallback = ih.get_str("url", option="operationCallback")
        # 拼接完整url
        url = Test_pushMiniPro.host + self.operationCallback
        log.info(f"operationCallback接口的地址是:{url}")
        data = {
            "additionalInfo": "additionalInfo1",
            "operationId": Test_pushMiniPro.operationId,
            "operationType": Test_pushMiniPro.operationType,
            "recordId": Test_pushMiniPro.recordId,
            "state": 0,
            "system": "lsxtest",
            "wechatId": Test_pushMiniPro.teacher_wechat,
            "versionName": "3.1.13",
            "versionCode": "97",
            "wechatAccount": Test_pushMiniPro.teacher_wechat,
            "wechatVersion": "7.0.5",
            "wechatVersionCode": "1440",
            "source": "app_root",
            "loginAccount": Test_pushMiniPro.account,
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

    @allure.story("推送小程序")
    @allure.title("测试推送小程序指令入库")
    @allure.description("描述：验证数据库中推送小程序指令status=-2")
    @allure.severity("critical")
    @allure.testcase("https://baidu.com", name="这是功能测试用例连接")
    @allure.issue("https://baidu.com", name="这是bug连接")
    @allure.step("第四步：验证数据库中推送小程序指令是status=0")
    @pytest.mark.run(order=8)
    def test_mysql_wechat_push_minipro2(self):
        if Test_pushMiniPro.operationId == "":
            pytest.xfail(reason="心跳接口没有取到指令，验证status操作标记失败")
        sql = 'SELECT * FROM wechat_push_minipro WHERE account = "dongfangyao" ORDER BY id DESC '
        result = mh.find_one(sql)
        log.info(f"wechat_auto_apply表中account=’dongfangyao‘的最新一条推送小程序数据是{result}")
        log.info(f"wechat_auto_apply表中recordId是{result[1]}")
        log.info(f"插入的recordId是{Test_pushMiniPro.recordId}")
        assert result[1] == Test_pushMiniPro.recordId, "最近一条数据的recordId是%s" % Test_pushMiniPro.recordId
        assert int(result[6]) == 0, "state字段是：%s" % result[7]
        log.info("wechat_auto_apply表中state值正确")
