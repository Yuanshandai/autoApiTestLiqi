
import pytest
from common.Logging_Handle import log


# login登录功能函数，实际工作中直接拿接口即可
def login(username=None, password=None) -> dict:
    """
    登录校验的函数
    :param username: 账号
    :param password:  密码
    :return: dict type
    """
    if all([username, password]):
        if username == 'admin' and password == '123456':
            return {"code": 0, "msg": "登录成功"}
        else:
            return {"code": 1, "msg": "账号或密码不正确"}
    else:
        return {"code": 1, "mgs": "所有的参数不能为空"}


data = [{"username": "admin", "pwd": "123456", "expect": '{"code": 0, "msg": "登录成功"}'},
        {"username": "admin", "pwd": "132456", "expect": '{"code": 1, "msg": "账号或密码不正确"}'},
        {"username": "", "pwd": "123456", "expect": '{"code": 1, "mgs": "所有的参数不能为空"}'},
        {"username": "admin", "pwd": "", "expect": '{"code": 1, "mgs": "所有的参数不能为空"}'}]


class TestLogin(object):

    @pytest.mark.parametrize("case", data)
    def test_login(self, case):
        username = case["username"]
        pwd = case["pwd"]
        expect = eval(case["expect"])
        result = login(username, pwd)
        try:
            assert expect == result, "预期与实际结果不相符"
            log.info("用例执行成功")
        except AssertionError as e:
            log.error("用例执行失败")
            raise e
