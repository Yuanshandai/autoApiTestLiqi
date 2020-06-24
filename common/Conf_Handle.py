
"""
*****配置文件*******
==== YamlHandle: 处理yaml配置文件=====
=====IniHandle:封装读取ini配置文件=====
====TxtHandle:封装读取txt配置文件===(数据库)========
"""
import os
from configparser import ConfigParser
from common.Path import CONF_DIR
import yaml

class YamlHandle(object):
    """处理yaml配置文件"""

    def __init__(self, file_name):
        self.file_name = file_name

    def __open(self):
        """
        打开yaml文件，读取全部的信息
        :return: yaml文件中的全部信息
        """
        with open(self.file_name, encoding="utf-8") as f:
            return yaml.load(f, yaml.FullLoader)

    def get_data(self, node):
        """
        读取对应节点的值
        :param node: 节点名称
        :return: 节点对应的值
        """
        return self.__open()[node]


class IniHandle(ConfigParser):
    """封装的读取ini/config配置文件类"""

    def __init__(self, file_name, encoding='utf8'):
        """
        初始化
        :param file_name: 配置文件名
        :param encoding: 编码格式
        """
        super().__init__()
        self.file_name = file_name
        self.encoding = encoding
        self.read(file_name, encoding=encoding)

    def get_str(self, section, option):
        return self.get(section, option)

    def get_int(self, section, option):
        return self.getint(section, option)

    def get_float(self, section, option):
        return self.getfloat(section, option)

    def get_boolean(self, section, option):
        return self.getboolean(section, option)

    def write_data(self, section, option, value):
        """
        添加值
        :param section: 配置块
        :param option: 配置属性
        :param value: 对应的配置属性值
        """
        self.set(section, option, value)
        self.write(open(self.file_name, 'w', encoding=self.encoding))



class TxtHandle(ConfigParser):
    """
    封装读取Txt/config配置文件的类
    """
    def __init__(self,filepath, encoding='utf8'):
        super().__init__()
        self.filepath = filepath
        self.encoding = encoding
        self.read(filepath, encoding=encoding)

    def get_str(self,param,database="database-test"):
        #默认查测试库
        #获取指定[]标签下的变量值
        return self.get(database,param)

    def get_int(self,param,database="database-test"):
        #默认查测试库
        #获取指定[]标签下的变量值
        return self.getint(database,param)

    def get_float(self,param,database="database-test"):
        return self.getfloat(database, param)

    def get_boolean(self, param, database="database-test"):
        return self.getfloat(database, param)


yaml_file = os.path.join(CONF_DIR, 'conf.yaml')
ini_file = os.path.join(CONF_DIR, 'conf.ini')
txt_file = os.path.join(CONF_DIR, "conf.txt")
yh = YamlHandle(yaml_file)
ih = IniHandle(ini_file)
th = TxtHandle(txt_file)



if __name__ == '__main__':


    t = th.get_str("port",database="database-data-center")
    print(t)
    print(type(t))

    t = th.get_int("port", database="database-data-center")
    print(t)
    print(type(t))