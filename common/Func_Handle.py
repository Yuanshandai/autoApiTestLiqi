"""
===封装一些功能函数====
===random_phone: 随机生成手机号码
"""

import random

start_phone = ['130', '131', "132", "133", "134", "135", "136", "137", "138", "139",
               "150", "151", "152", "153", "155", "156", "157", "158", "159", "180",
               "181", "182", "183", "184", "185", "186", "187", "188", "189"]


def random_phone():
    """
    随机生成手机号
    :return: 随机生成的手机号
    """
    phone = start_phone[random.randint(0, len(start_phone) - 1)]
    for i in range(8):
        phone += str(random.randint(0, 9))
    return phone

if __name__ == '__main__':
    phone = random_phone()
    print(phone)
