#!/usr/bin/python3
# -*- coding: UTF-8 -*-

'''
本文件为python创建适用于mysql数据库的操作语句，可以在python3文件中使用
明天工作内容：1、mysql与python3连接；  2、 mysql的增、删、改、查sql语句封装成可以被python3调用的方法
'''
import os
import pymysql
from configparser import ConfigParser


dir_config_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'monitor_system\config_file\db_config.ini')  # 获取数据库配置文件
cf = ConfigParser()
cf.read('D:/Git_Reposition_Location/monitor/monitor_system/config_file/db_config.ini')
host = cf.get('mysqlconf', 'host')
port = cf.get('mysqlconf', 'port')
user = cf.get('mysqlconf', 'user')
password = cf.get('mysqlconf', 'password')
db_name = cf.get('mysqlconf', 'db_name')

class mysql_db():
    def __init__(self):
        '''
        初始化：建立mysql与pythond3的链接
        return:返回一个已连接的数据库对象
        '''
        self.conn = pymysql.connect(host, user,password, db_name, charset = 'utf8')    # 连接数据库
        self.cur = self.conn.cursor()                                                   # 建立游标

    def close(self):
        '''
        关闭mysql数据库连接
        :return:
        '''
        self.cur.close()
        self.conn.close()

    def select(self, table, fieldname=None, data=None):
        '''
        查询语句
        :param table: 数据库monitor_system中表名
        :param fieldname 表中字段名称
        :param interfacename: 接口名称
        :return:
        '''
        if fieldname != None:   # 按条件查询
            sql = 'select * from '+ table + ' where %s = "%s";' % (fieldname, data)
        else:        # 查询表中所有数据
            sql = 'select * from %s;' %table
        self.cur.execute(sql)
        results = self.cur.fetchall()
        index = self.cur.description  # 获取查询数据的字段名称及其描述
        return results, index

    def access_result(self, results, index):
        '''
        目的：用于获取查询sql语句的查询结果
        :param results: 为查询的sql语句使用fectchall方法返回的结果
        :param index: 为执行查询后，使用self.cur.description获取的字段名称及属性
        :return: 返回一个由字典组成的列表，列表中每个元素（即字典）是一条数据，字典由字段名和值组成
        '''
        result = []
        for res in results:
            row = {}
            for i in range(len(index)):
                row[index[i][0]] = res[i]  # 将每个字段名和相应的值添加到字典row中
            result.append(row)
        return result

    def update(self):
        '''
        更新数据库数据
        :return:
        '''
        pass

    def insert(self):
        '''
        插入数据
        :return:
        '''
        pass

    def delete(self):
        '''
        插入数据
        :return:
        '''
        pass


if __name__ == '__main__':
    '''
    db = mysql_db()
    results,index = db.select('mn_system_interface_to_developer')
    r = db.access_result(results, index)
    print(r)
    db.close()
    '''
    db = mysql_db
    print(type(db))
    db1 = mysql_db()
    print(type(db1))
