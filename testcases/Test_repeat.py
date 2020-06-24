# -*-coding:GBK -*-
import pytest


class Test_repeat:
    def test_repeat3(self):
        print("测试用例执行333")
@pytest.mark.repeat(5)
class Test_repeat2:
    def test_repeat3(self):
        print("测试用例执行444")


if __name__ == "__main__":
    pytest.main(["-s", "Test_repeat.py"])
