# encoding=utf8
import pymysql


class connect:
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='xiaoqi',
            password='zhaoben1018',
            db='api_project',
            charset='utf8'
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        #在创建游标时尽量为字典形式:cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    def __del__(self):
        self.conn.commit()
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭连接

# class MysqlHelper():
#     def __init__(self, host, port, db, user, passwd, charset='utf8'):#初始化登陆参数
#         self.host = host#127.0.0.1
#         self.port = port#端口
#         self.db = db#数据库名
#         self.user = user#用户名
#         self.passwd = passwd#用户密码
#         self.charset = charset#编码方式
#
#     def connect(self):#数据库连接及数据库路由创建
#         self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,
#                                     charset=self.charset)
#         self.cursor = self.conn.cursor()
#
#     def close(self):#数据库连接及数据库路由关闭
#         self.cursor.close()
#         self.conn.close()
#
#     def get_one(self, sql, params=()):
#         result = None
#         try:
#             self.connect()
#             self.cursor.execute(sql, params)
#             result = self.cursor.fetchone()
#             self.close()
#         except Exception as e:
#             print(e.message)
#         return result
#
#     def get_all(self, sql, params=()):
#         list = ()
#         try:
#             self.connect()
#             self.cursor.execute(sql, params)
#             list = self.cursor.fetchall()
#             self.close()
#         except Exception as e:
#             print(e.message)
#         return list
#
#     def insert(self, sql, params=()):
#         return self.__edit(sql, params)
#
#     def update(self, sql, params=()):
#         return self.__edit(sql, params)
#
#     def delete(self, sql, params=()):
#         return self.__edit(sql, params)
#
#     def __edit(self, sql, params):
#         count = 0
#         try:
#             self.connect()
#             count = self.cursor.execute(sql, params)
#             self.conn.commit()
#             self.close()
#         except Exception as e:
#             print(e.message)
#
#         return count

