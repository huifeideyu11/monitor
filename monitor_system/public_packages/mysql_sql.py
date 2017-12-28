#!/usr/bin/python3
# -*- coding: UTF-8 -*-

'''
本文件为python创建适用于mysql数据库的操作语句，可以在python3文件中使用
明天工作内容：1、mysql与python3连接；  2、 mysql的增、删、改、查sql语句封装成可以被python3调用的方法
'''
import os
import pymysql
from configparser import ConfigParser


dir_config_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config_file\db_config.ini')  # 获取数据库配置文件
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

    def select(self, sql):
       '''
       :param sql:
       :return:
       '''
       pass


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
    #db = pymysql.connect(host=host, user=user, password=password, db=db_name)
    print('%s,%s,%s,%s' %(host, user, password, db_name))
