import pymysql
import redis
from common.Conf_Handle import th


# 读数据库配置信息

class MysqlHandle(object):
    """封装MySql数据库操作"""

    def __init__(self, use_database):
        # 创建数据库连接
        self.con = pymysql.connect(host=th.get_str("host", use_database),
                                   port=th.get_int("port", use_database),
                                   database=th.get_str("database", use_database),
                                   user=th.get_str("user", use_database),
                                   password=th.get_str("password", use_database),
                                   charset=th.get_str("charset", use_database),
                                   )
        # print("连接成功了")
        # 创建游标
        self.cur = self.con.cursor()

    def find_one(self, sql) -> tuple:
        """
        查找返回第一条数据
        :param sql:
        :return:
        """
        try:
            self.con.commit()
            self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception as e:
            self.con.rollback()
            print("method: find_one execute Failed", e)

    def find_all(self, sql) -> tuple:
        """
        查找返回所有数据
        :param sql:
        :return:
        """
        try:
            self.con.commit()
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            self.con.rollback()
            print("method:find_all execute Failed", e)

    def count(self, sql) -> int:
        """
        返回数据条数
        :param sql:
        :return:
        """
        try:
            self.con.commit()
            return self.cur.execute(sql)
        except Exception as e:
            self.con.rollback()
            print("method:count execute Failed", e)

    def close(self):
        """关闭游标对象和断开连接"""
        try:
            self.cur.close()
            self.con.close()
        except Exception as e:
            print("method:close execute Failed", e)

    def execute_sql(self, sql, data=None):
        """
        执行sql并提交
        :param sql:需要执行的sql
        :return:
        """
        # 将要插入的数据写成元组传递
        # print("执行了插入操作：")
        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            print("method:execute_sql execute Failed!", e)

    def select_save(self, sql, index=0) -> list:
        """
        得到查询结果的某一列并保存到list中(默认第0列)
        :param sql:
        :return:
        """
        datalist = []
        try:
            self.cur.execute(sql)
        except Exception as e:
            self.con.rollback()
            print("method:select_save execute Failed!", e)

        results = self.cursor.fetchall()
        for i in results:
            datalist.append(i[index])
        # 去重
        return list(set(datalist))


class RedisHandle(object):
    """封装redis数据库操作 """

    def __init__(self, use_database):

        # 创建连接池
        self.pool = redis.ConnectionPool(host=th.get_str("host", use_database),
                                         port=th.get_int("port", use_database),
                                         password=th.get_str("password", use_database),
                                         decode_responses=True)


        # 创建数据库连接
        self.con = redis.Redis(connection_pool=self.pool)

    def str_get(self, key) -> str:
        """
        查询字符串
        :param key:
        :return:
        """
        return self.con.get(key)

    def str_set(self, key, value, time=None):  # time默认失效时间
        """
        插入字符串
        :param key:
        :param value:
        :param time:
        :return:
        """
        self.con.set(key, value, time)

    def delete(self, key):
        """
        删除指定的键值
        :param key:
        :return:
        """
        tag = self.con.exists(key)
        # 判断这个key是否存在,相对于get到这个key他只是传回一个存在或者不存在的信息，
        # 而不用将整个k值传过来（如果k里面存的东西比较多，那么传输很耗时）
        if tag:
            self.con.delete(key)
        else:
            print('这个key不存在')

        # self.con.delete(key) if self.con.exists(key) else print('这个key不存在')

    def hash_get(self, name, key) ->str:  # 哈希类型存储的是多层字典（嵌套字典）
        """
        得到哈希类型的key对应的键值
        :param name:
        :param key:
        :return:
        """
        return self.con.hget(name, key)


    def hash_set(self, name, key, value):  # 哈希类型的是多层
        """
        设置hash类型的键对应的值
        :param name:
        :param key:
        :param value:
        :return:
        """
        self.con.hset(name, key, value)  # set也不会报错

    def hash_getall(self, name) -> dict:
        """
        得到hash类型的所有键值,存储到字典中
        :param name:
        :return:
        """
        res = self.con.hgetall(name)  # 得到的是字典类型的，里面的k,v都是bytes类型的
        data = {}
        if res:
            for k, v in res.items():  # 循环取出字典里面的k,v，在进行decode
                data[k] = v
        return data

    def hash_del(self, name, key):
        """
        删除hash类型的key的键值
        :param name:
        :param key:
        :return:
        """
        res = self.con.hdel(name, key)
        if res:
            print('删除成功')
            return 1
        else:
            print('删除失败，该key不存在')
            return 0

    @property  # 属性方法，
    # 使用的时候和变量一个用法就好比实例，A=MyRedis(), A.clean_redis使用，
    # 如果不加这个@property,使用时A=MyRedis(), A.clean_redis()   后面需要加这个函数的括号
    def clean_redis(self):
        """
        清空key值
        :return:
        """
        self.con.flushdb()  # 清空 redis
        print('清空redis成功！')
        return 0
    #----------------------------------
    def list_get(self, key,first = 0,last =-1) ->list:
        """
        得到list类型的key对应的键值
        :param key: 键
        :param first: 起始位置默认0
        :param last: 结束为止默认-1
        :return:
        """
        return self.con.lrange( key,first,last)

    def list_getone(self, key,first = -1,last =-1) ->dict:
        """
        得到list类型的队列最右一个字符串转成字典类型
        :param key: 键
        :param first: 起始位置默认0
        :param last: 结束为止默认-1
        :return:
        """
        list1 = self.con.lrange(key, first, last)
        #list1[0].replace("true", "True")
        if(len(list1)>0):
            return eval(list1[0].replace("true", "True"))
        else:
            print("队列里没有指令！")

    def list_lpush(self, key, value):  # 哈希类型的是多层
        """
        添加一个元素在列表头部
        :param name:
        :param key:
        :param value:
        :return:
        """
        self.con.lpush( key, value)

    def list_rpush(self,key, value):  # 哈希类型的是多层
        """
        添加一个元素在lsit尾部
        :param name:
        :param key:
        :param value:
        :return:
        """
        self.con.rpush( key, value)  # set也不会报错



class EsHandle(object):
    """封装es数据库操作
    TODO:es数据库操作-暂未封装
    """


mh = MysqlHandle("database-wechat")
rh = RedisHandle("redis-test")


if __name__ == '__main__':
    # # 传入标签值 "database-test"
    # test = MysqlHandle("database-test")
    # sql = "select * from t_kant_class_info "
    # result = test.find_all(sql)
    # result1 = test.find_one(sql)
    # result2 = test.count(sql)
    # # 执行插入
    # sql1 = "insert into t_kant_class_into "
    # test.execute_sql(sql1)
    # print(result2)

     test1 = RedisHandle("redis-test")
     # print(test1.str_get("liqi"))
     # print(type(test1.str_get("liqi")))
    # test1.str_set("liqi1","hhhh")
    # print(test1.str_get("liqi1"))
    # test1.delete("liqi")
    # print(test1.str_get("liqi"))

     # print(test1.hash_get("liqi","test1111"))
     # test1.hash_set("liqi","test3","!")
     # print(test1.hash_get("liqi","test3"))
     # print(test1.hash_getall("liqi"))

     # print(test1.list_get("q"))
     # print(type(test1.list_get("q")))
     # print(type(test1.list_get("q",-1,-1)))



     # list1 = test1.list_get("wxid_ss245739845_{apply_friend_list}",0,-1)
     # print(list1)
     # print(type(list1))
     # print(type(list1[0]))
     # list1[0].replace("true","True")
     # print(type(eval(list1[0].replace("true","True"))))
     # print(eval(list1[0].replace("true","True")))

     print(test1.list_getone( "wxid_ss245739845_{apply_friend_list}" ))

