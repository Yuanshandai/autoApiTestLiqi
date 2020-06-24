"""
=== Excel操作 ===
=== CaseData: 保存数据类 ===
=== ExcelHandle: 处理Excel文件 ===
"""
import os
import openpyxl
from common.Path import DATA_DIR

class CaseData(object):
    pass

class ExcelHandle(object):
    """处理Excel文件"""

    def __init__(self,file_name,sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def __open(self):
        self.wb = openpyxl.load_workbook(self.file_name)
        self.sh = self.wb[self.sheet_name]

    def get_data_dict(self) -> dict:
        """读取数据存储在字典中"""
        self.__open()
        rows = list(self.sh.rows)
        return [dict(zip([i.value for i in rows[0]],[r.value for r in row]))
                for row in rows[1:]]

    def get_data_obj(self) -> list:
        """读取数据存储在类中"""
        self.__open()
        rows = list(self.sh.rows)
        # 定义用例列表，用来存放用例类列表
        cases = []
        # 遍历用例数据行
        for row in rows[1:]:
            # 把每一行的数据通过zip进行打包，然后转成字典，存入到用例数据列表中
            case = dict(zip([i.value for i in rows[0]],[r.value for r in row]))
            # 定义一个用例存放类对象
            case_obj = CaseData()
            for k,v in case.items():
                # 通过setattr()给对象添加属性
                setattr(case_obj,k,v)
            # 把对象添加到列表中
            cases.append(case_obj)
        return cases

if __name__ == '__main__':
    file = os.path.join(DATA_DIR,"test1.xlsx")
    eh = ExcelHandle(file,"ts")
    data = eh.get_data_obj()
   # print(d.a for d in data)
    print([d.a for d in data])