# -*-coding:GBK -*-
import pytest
import allure
@allure.title("�������{name},{phone},{age}")
@pytest.mark.parametrize("name,phone,age", [
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9)
])
@allure.description("���Ƕ�������������ûɶ����")
def test_test_test(name, phone, age):
    print(name, phone, age)

if __name__ =="__main__":
    pytest.main(["-s", "Test_case1_add_friend.py"])