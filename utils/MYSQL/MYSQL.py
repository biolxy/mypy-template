#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : MYSQL.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2020-04-04 12:22:11
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import pymysql
import pandas as pd


class MYSQL(object):
    """
    对pymssql的简单封装 https://www.jb51.net/article/77728.htm
    pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启
    ref : https://www.jianshu.com/p/76fab6cb06f9
    """
    def __init__(self, db_host, db_user, db_pass, db_name, db_port=3306):
        self.host = db_host
        self.user = db_user
        self.pwd = db_pass
        self.db = db_name
        self.port = db_port

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
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
        # self.__CloseConn()
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
        # self.__CloseConn()

        # def ExecSQLcommit(self):
        #     self.conn.commit()
        #     self.conn.close()


if __name__ == '__main__':
    pass
    # conn = ANNOMYSQL()
    # sql = "SELECT * FROM 突变说明"
    # df = conn.ExecSQLRead(sql)
    # print(df)

