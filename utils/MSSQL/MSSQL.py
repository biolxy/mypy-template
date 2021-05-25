#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : MSSQL.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2020-11-17 13:31:46
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import pymssql
import pandas as pd
from sqlalchemy import create_engine


class MSSQL(object):
    """
    对pymssql的简单封装 https://www.jb51.net/article/77728.htm
    pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启
    用法：
    """
    def __init__(self, db_host, db_user, db_pass, db_name):
        self.host = db_host
        self.user = db_user
        self.pwd = db_pass
        self.db = db_name

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,
                                    user=self.user,
                                    password=self.pwd,
                                    database=self.db,
                                    charset="utf8")
    
    def __CloseConn(self):
        self.conn.close()

    def ExecSQLRead(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        调用示例：
        ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
        df = ms.ExecSQL("SELECT id,NickName FROM WeiBoUser")
        """
        self.__GetConnect()
        df = pd.read_sql_query(sql, self.conn)
        self.__CloseConn()
        return df

    def ExecSQLWRITE(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        调用示例：
        ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
        df = ms.ExecSQL("SELECT id,NickName FROM WeiBoUser")
        """
        self.__GetConnect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
        self.__CloseConn()

    def ExecSQLWRITE2(self, df, name):
        con = create_engine("mssql+pymssql://{user}:{pwd}@{host}/{db}?charset=utf8".format(
                user= self.user,
                pwd=self.pwd,
                host=self.host,
                db=self.db,
        ))
        df.to_sql(name=name, con=con, if_exists='append', index=False)
        con.dispose()
        # self.__CloseConn()

# if __name__ == '__main__':
#     main()
