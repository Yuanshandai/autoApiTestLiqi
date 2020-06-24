"""
=== 数据参数化 ===
=== replace_data:数据参数格式化
=== ReplaceData:临时保存一些要替换的数据
"""

import re
from configparser import NoOptionError

from common.Conf_Handle import ih
class ReplaceData:
    """临时保存一些要替换的数据"""
    pass

def replace_data(case_data):
    """数据参数格式化"""
    #匹配规则
    r = "#(.+?)#"
    #判断匹配结果是否是None
    while re.search(r,case_data):
        # 匹配出第一个要替换的内容
        res = re.search(r,case_data)
        # 提取待替换的内容
        item = res.group()
        # 获取替换内容的数据项
        key = res.group(1)
        try:
            case_data = case_data.replace(item,ih.get_str("data",key))
        except NoOptionError:
            case_data = case_data.replace(item,str(getattr(ReplaceData,key)))

    return case_data

if __name__ == '__main__':
    data = '{"mobile_phone": "#account#", "pwd": "#pwd#", "reg_name":"#reg_name#"}'
    setattr(ReplaceData, "reg_name", "小明")
    print(replace_data(data))