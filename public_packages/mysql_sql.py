#!/usr/bin/python3
# -*- coding: UTF-8 -*-

'''
本文件为python创建适用于mysql数据库的操作语句，可以在python3文件中使用
明天工作内容：1、mysql与python3连接；  2、 mysql的增、删、改、查sql语句封装成可以被python3调用的方法
'''
import os
import pymysql, json, types
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
                row[index[i][0]] = res[i]  # 将每个字段名和相应的值添加到字典row中，index[i][0]获取字段名
            result.append(row)
        return result

    def update(self):
        '''
        更新数据库数据
        :return:
        '''
        pass

    def insert_new(self, tablename, data):
        '''

        :param tablename: 表名
        :param data: 字典类型，键值分别由字段名和数据组成
        :return: 无
        注：插入语句中的列名，不能以元组的形式通过.format进行传入，如何这样操作，sql语句中的列名会变成字符串，则出现语法错误
        '''
        key_str = ''
        values_str = []
        for key in data:
            key_str += key + ","
            if data[key] == None:
                data[key] = 'null'  # 数据库中防止同时存入空字符串和null，此处做处理
            if isinstance(data[key], dict):
                data[key] = json.dumps(data[key], ensure_ascii=False)    # 将pyton格式数据转换成json格式数据，ensure_ascii=False参数表示允许acsii之外的字符显示
                data[key] = pymysql.escape_string(data[key])
                data[key] = data[key].replace('\\', '')     # 将转义字符去掉
                # print('转以后数据：', data[key])
            values_str.append(data[key])


        key_str = key_str.rstrip(',')  # 去掉字符串右侧的'，'
        values_str = tuple(values_str)
        print(values_str)
        sql1 = "insert into {0} ({1}) values {2}".format(tablename, key_str, values_str)
        # print('sql1的值是：', sql1)
        self.cur.execute(sql1)
        self.conn.commit()       # 提交到数据库

    def delete(self):
        '''
        插入数据
        :return:
        '''
        pass



if __name__ == '__main__':

    data = {'return_value': {'mobileBindStatus': True, 'result': True, 'errorMsg': '成功', 'errorCode': 0},
            'interface_name': '登录接口', 'login_result': 'success', 'reason': None, 'result': 'success',
            'abnormal': None, 'request_time': '2018-01-08 11:37:12'}

    db = mysql_db()
    # results,index = db.select('mn_system_interfacelist')
    # print(db.access_result(results, index))
    # db.test(data)
    # db.insert('mn_system_interfacelist', data)
    db.insert_new('mn_system_interfacelist', data)
    db.close()

    '''
    d = {'mobileBindStatus': True, 'result': True, 'errorMsg': 'success', 'errorCode': 0}
    d_j  = json.dumps(d)

    print(pymysql.escape_string(d_j))
    print(type(pymysql.escape_string(d_j)))
    data = {'id': 6, 'return_value': d_j}
    db = mysql_db()
    sql = "insert into test2 (id, return_value) values ('5', '{}')".format(pymysql.escape_string(d_j))

    print(sql)
    db.cur.execute(sql)
    db.conn.commit()
    db.close()
    '''






