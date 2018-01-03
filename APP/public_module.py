#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import traceback, re
from Auto_mail import send_mail,time_c, time_n
from requests.adapters import HTTPAdapter
from public_packages.mysql_sql import mysql_db


def sendmsg(terminal, phonenum, msg_text, time_s='', filename1='', filename2=''):
    '''
    用途：发送异常短信
    参数：
        terminal：终端类型，APP或者PC官网
        phonenum：为手机号码组成的str类型，多个手机号码用逗号隔开；如：'13694917391,15361431731'
        msg_text：短信发送内容及短信发送异常后发送邮件通知的正文
        filename1:文件路径+文件名，为记录操作记录的文件
        filename2:文件路径+文件名，为记录错误日志的文件
        time_s：操作记录文本的时间,str类型
    :return: 无
    '''
    ###############邮件发送数据################
    server = {'username': 'yongsheng.luo@xiu.com', 'psw': '19910204514liu', 'host': "smtp.xiu.com", 'port': 25}
    from_addr = 'yongsheng.luo@xiu.com'
    to_addr = ['631442624@qq.com', 'yongsheng.luo@xiu.com']   # 短信发送异常邮件通知人
    subject = '【下单监控】' + terminal + '：短信发送失败'

    msg = '【下单监控{}】'.format(terminal)  + '在' + msg_text    # 短信信息 msg_text为监控异常邮件发送的正文
    lenth = len(phonenum.split(','))

    s_sendmsg = requests.session()
    s_sendmsg.mount('http://', HTTPAdapter(max_retries=3))    # 设置请求访问失败的重试次数

    url = 'http://ws.montnets.com:9002/MWGate/wmgw.asmx/MongateCsSpSendSmsNew?' \
          'userId=J30173&password=080056&pszMobis={0}&pszMsg={1}&iMobiCount={2}&' \
          'pszSubPort=106571014054499'.format(phonenum, msg, lenth)

    try:
        r = s_sendmsg.get(url, timeout=30)
        print('短信发送成功')
        #print('短信请求返回值：', r.text)
        with open(filename1, 'a') as f:   # 将短信发送失败记录写入操作记录文件中
            f.write('{}：短信发送成功'.format(time_s) + '\n')
        s_sendmsg.close()  # 关闭会话

    except:
        print('短信发送失败')

        with open(filename1, 'a') as f:   # 将短信发送失败记录写入操作记录文件中
            f.write('{}：短信发送失败'.format(time_s) + '\n')

        sendmsg_error = traceback.format_exc()   # 获取报错信息
        with open(filename2, 'w') as f:         # 将错误信息写入附件中，
            f.write(sendmsg_error)
        send_mail(server, from_addr, to_addr, subject, text=msg_text, files=[filename2])  # 短信异常发送邮件
        s_sendmsg.close()  # 关闭会话

class monitor():

    def accessEmail(self, table, fieldname=None, data=None):
        '''
            :param table: 数据库monitor_system中表名
            :param fieldname 表中字段名称
            :param interfacename: 接口名称
            :return:返回一个元组由两个字典，由接口名称和对应的报警邮箱地址组成的键值对组成
        '''
        emailaddress = {}
        phones = {}
        db = mysql_db()                        # 连接monitor_system数据库
        results, index = db.select(table, fieldname=None, data=None)
        re = db.access_result(results, index)
        for i in range(len(re)):
            emailaddress[re[i]['interface_name']] = re[i]['email']
            phones[re[i]['interface_name']] = re[i]['phone']

        db.close()
        return emailaddress, phones

    def interface_email(self, emailaddress, interfacename):
        '''
        目的：将同一接口的邮件地址存放在一个列表中
        :param emailaddress: 字典类型，键值对是由接口名和对应的邮件报警人邮箱组成，值是字符串类型
        :param interfacename:接口名
        :return: 返回一个列表，存放同一接口的报警通知人邮件地址，
        '''
        email = emailaddress[interfacename]                  # 获取指定接口的所有邮件报警人地址
        to_addr = re.split(',|，', email)                    # 用“,”和“，”进行分割字符串（“，”分别是中文和英文版的逗号）
        return to_addr

    def interface_phone(self, phones, interfacename):
        '''
            目的：同一接口对应的开发手机号拼接成符合短信发送要求的字符串
            :param emailaddress: 字典类型，键值对是由接口名和对应的开发手机号组成，值是字符串类型
            :param interfacename:接口名
            :return: 返回字符串，由同一个接口对应的所有报警通知人员的手机号拼接而成，
        '''
        phonenums = re.split(',|，', phones[interfacename])    # 将同一接口的电话号码，进行分割，返回的是一个列表
        phone = ''
        for phonenum in phonenums:
            if len(phonenums) == 1:
                phone = phonenums[0]
                break
            phonenum = phonenum +','
            phone += phonenum
        return phone.rstrip(',')

    def interfaceRequestResult(self, data, tablename='mn_system_interfacelist'):
        '''
        目的：用于将接口调用产生的数据插入到数据库表：mn_system_interfacelist中
        :param data: 字典类型，需要插入的数据（数据为：接口调用产生的数据）
        :param tablename: 数据库中表名
        :return:
        '''
        db = mysql_db()                # 连接数据库
        db.insert(tablename=tablename, data=data)    # 将接口调用的数据插入到数据库中
        db.close()               # 关闭数据库连接


if __name__ == '__main__':

    '''
    url = 'http://ws.montnets.com:9002/MWGate/wmgw.asmx/MongateCsSpSendSmsNew?' \
          'userId=J30173&password=080056&pszMobis={0}&pszMsg={1}&iMobiCount={2}&' \
          'pszSubPort=106571014054499'.format('13684995613', '短信测试', 1)
    r = requests.get(url, timeout=60)
    print('短信发送成功')
    email_login = accessEmail('mn_system_interface_to_developer')[0]['登录接口']
    to_addr_l1 = email_login.split(' ')
    print(to_addr_l1)
    to_addr_l = re.split(",|，", email_login)
    print(to_addr_l)
    '''
    monitor = monitor()
    print(monitor.accessEmail('mn_system_interface_to_developer'))
    emailaddress, phones = monitor.accessEmail('mn_system_interface_to_developer')
    print(monitor.interface_email(emailaddress, '登录接口'))
    print(monitor.interface_phone(phones, '登录接口'))
