# -*-coding:GBK -*-
import pytest
import allure
@allure.title("多个参数{name},{phone},{age}")
@pytest.mark.parametrize("name,phone,age", [
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9)
])
@allure.description("这是对用例的描述，没啥大用")
def test_test_test(name, phone, age):
    print(name, phone, age)

if __name__ =="__main__":
    pytest.main(["-s", "Test_case1_add_friend.py"])