#!/usr/bin/python3
# coding = utf-8

import requests, traceback
from bs4 import BeautifulSoup
import time, json, random
from Auto_mail import send_mail,time_c, time_n, access_hour
from assertpy import assert_that
from requests.adapters import HTTPAdapter
from public_module import sendmsg, accessEmail
from public_module.monitor import accessEmail, interface_email, interface_phone

'''
    注：
        1、所有报错都统一处理，没有细分报错。此处有可能出现的报错有：服务器拒绝的HTTPError；访问超时的
        requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout；返回值Json解析错误:
        json.decoder.JSONDecodeError；
        2、本程序逻辑：1、首先调登陆接口，若登陆失败，退出程序；2、登陆成功后，调用搜索、购物车、下单接口（搜索、
        购物车、下单接口调用是并列关系，无关联）； 3、购物车接口包括：商品添加购物车接口和删除购物车商品；4、下单接口
        包括：提交订单、取消订单、删除订单接口
'''

'''
#########################短信发送数据##########################
# ----注意：phonenum_l、phonenum_s、phonenum_a、phonenum_o 变量值为多个号码中间用逗号隔开，但是不留空格
# phonenum_l: 登录接口相关人员;       phonenum_s: 搜索接口相关人员
# phonenum_a: 购物车接口相关人员;     phonenum_o: 下单接口相关人员
phonenum_l = '13694917391,13684995613,15919451736,18675583403,13339916922,18320989189,17704003244'
phonenum_s = '13694917391,13684995613,13410547406,18675583403,13339916922,18320989189,17704003244'
phonenum_a = '13694917391,13684995613,13692230821,15999969165,18675583403,13339916922,18320989189,17704003244'
phonenum_o = '13694917391,13684995613,13480794537,15013732515,17704003244,13692230821,15999969165,18675583403,13339916922,18320989189'


######################### 邮件数据 ######################
server = {'username':'monitor@xiu.com', 'psw':'zoshow$%^456', 'host':"smtp.xiu.com", 'port':25}  # 邮件配置数据
from_addr = 'monitor@xiu.com'     # 邮件发送者

to_addr_l = ['michelle.jia@xiu.com', 'yongsheng.luo@xiu.com', 'benson.shi@xiu.com',
             'fc.li@xiu.com', 'bin.liao@xiu.com', 'deny.liu@xiu.com', 'mike.gao@xiu.com']   # 登录接口相关人员

to_addr_s = ['michelle.jia@xiu.com', 'yongsheng.luo@xiu.com', 'rian.luo@xiu.com',
             'fc.li@xiu.com', 'bin.liao@xiu.com', 'deny.liu@xiu.com', 'mike.gao@xiu.com']   # 搜索接口相关人员

to_addr_a = ['michelle.jia@xiu.com', 'yongsheng.luo@xiu.com', 'simon.li@xiu.com',
             'jeff.hong@xiu.com', 'fc.li@xiu.com', 'bin.liao@xiu.com', 'deny.liu@xiu.com', 'mike.gao@xiu.com']   # 添加购物车接口相关人员

to_addr_o = ['michelle.jia@xiu.com', 'yongsheng.luo@xiu.com', 'stone.xia@xiu.com', 'long.yu@xiu.com',
             'mike.gao@xiu.com', 'simon.li@xiu.com', 'jeff.hong@xiu.com', 'fc.li@xiu.com',
             'bin.liao@xiu.com', 'deny.liu@xiu.com']   # 下单接口相关人员

'''
terminal = 'APP测试'       # 终端分类标志，被写入到邮件的主题以及短信中，如果是本地调试，请注明调试字样，
server = {'username':'monitor@xiu.com', 'psw':'zoshow$%^456', 'host':"smtp.xiu.com", 'port':25}  # 邮件配置数据
from_addr = 'monitor@xiu.com'     # 邮件发送者

emailaddress, phones = accessEmail('mn_system_interface_to_developer')     # 从数据库中获取接口报警的邮箱地址和手机号

# --- 获取接口邮件报警通知人员的邮箱地址 --- #
to_addr_l = interface_email(emailaddress, '登录接口')
to_addr_s = interface_email(emailaddress, '搜索接口')
to_addr_a = interface_email(emailaddress, '购物车接口')
to_addr_o = interface_email(emailaddress, '订单接口')

# --- 获取接口的短信报警人的电话 ---#
phonenum_l = interface_phone(phones, '登录接口')
phonenum_s = interface_phone(phones, '搜索接口')
phonenum_a = interface_phone(phones,'购物车接口')
phonenum_o = interface_phone(phones, '订单接口')


# 从配置文件中读取文件的路径
files_l = []
with open('D:\luotian\Pycharm_Project\InterFace_test\order_process_monitor_app\\' +
          'app_report_location.txt', 'r', encoding='utf-8') as f:
    files = f.readlines()

for i in range(0, len(files)):
    file = files[i].rstrip(',\n')
    files_l.append(file)
print(files_l)


##################### 请求失败标志 ############
error_login_num = 0    # 登录失败次数
error_search_num = 0   # 查询失败次数
error_add_num = 0      # 添加购物车失败次数
error_submit_num = 0   # 订单创建失败次数

####################### 请求数据 ########################
params_login = {
                'encryptFlag':'Y',
                'loginChannel':'android',
                'memberVo.isRemember':1,
                'memberVo.regType':'02',
                'memberVo.password':	'MLlwRATkOs/4b3DLy8xlOQ==',
                'memberVo.logonName': '13694917391'
}        # 登录params参数

data_search = {'kw': '测试', 'p':1, 'v': 2.0,
               'pSize': 20, 'src':'app',
               }    # 搜索请求表单数据

params_add = {
                'goodsSn':	17007288,
                'goodsSku':'170072880001',
                'quantity':1,
                'checked':'Y',
                'goodsSource':'UC1000'
}     # 添加购物车params参数

data_delshop = {'goodsSkus':'170072880001'}   # 删除购物车商品提交的表单数据

data_submit = {
                'goodsSn':	17007288,
                'goodsSku':'170072880001',
                'quantity':1,
                'orderReqVO.deliverTime':1,
                'orderReqVO.paymentMethod':	'ALIPAY_WIRE_APP',
                'orderReqVO.addressId':'8e1f2890ea53df0edf6d9a92cc4e785d',
                'orderReqVO.invoice':0,
                'orderReqVO.orderSource':3,
                'orderReqVO.goodsFrom':'UC1000',
                'm_cps_from_channel':'xiu-app',
                #'couponCode':'',   非必要的值
                'isVirtualPay':0,
                #'activeId':'',     非必填值
}   # 提交订单的表单数据

params_cancel = {}   # 取消订单的params参数

params_delete = {}   # 删除订单的params参数

url_login = 'http://mportal.xiu.com/loginReg/requestSubmitLogin.shtml'   # 登录连接
url_search = "http://mbrand.xiu.com/search/goodsList"
url_add = 'http://mportal.xiu.com/shoppingCart/addGoods.shtml'  # 加入购物车连接
url_delshop = 'https://mportal.xiu.com/shoppingCart/delGoods.shtml' # 删除购物车商品 post请求
url_submit = "http://mportal.xiu.com/order/createOrder.shtml"   # 生成订单连接
url_cancel = "http://mportal.xiu.com/order/cancelOrder.shtml"   # 取消订单
url_delete = "http://mportal.xiu.com/order/deleteOrder.shtml"   # 删除订单

headers = { 'User-Agent': 'okhttp/2.5.0'}


# ----------------------------程序运行-------------------------------- #
for i in range(1,2):
    print('APP下单监控程序开始')
    time_1 = time.time()     # 记录循环还是时间
    print('第%d次循环' %i)
    headers = {'User-Agent': 'okhttp/2.5.0'}
    s = requests.session()
    s.mount('http://', HTTPAdapter(max_retries=3))   # 设置HTTP请求失败，重试访问次数
    s.mount('https://', HTTPAdapter(max_retries=3))  # 设置HTTPS请求失败，重试访问次数

    ##################### 用户登录请求 #######################
    try:
        time_f = time_n()
        r_login = s.get(url_login, headers=headers, params=params_login, timeout=0.01)
        time.sleep(random.randint(0,10))
        print(r_login.json())
        r_login_j = r_login.json()     # 当返回的json格式不规范时，此处有可能出现json解析报错

        #if r_login_j['errorCode'] == 0 and r_login_j['errorMsg'] == '成功':
        if r_login_j['errorCode'] == 0 and r_login_j['errorMsg'] == '成功':
            print('登录成功')
            with open(files_l[9], 'a') as f:
                f.write("%s：用户【%s】登录成功" % (time_f, params_login['memberVo.logonName']) + '\n')

        else:
            # 获取返回的Json值，但是返回值错误，发送邮件

            error_login_num = 1    # 登录失败，返回值异常标志
            print('APP登录返回值验证失败')
            with open(files_l[9], 'a') as f:  # 记录登录操作
                f.write("%s：用户【%s】登录失败，请求返回值验证错误" % (time_f, params_login['memberVo.logonName']) + '\n')
            subject = '【下单监控】APP：登录失败'
            text = "%s：用户【%s】登录失败。\n\n请求返回值验证错误，返回值见邮件附件\n\n" \
                   % (time_f, params_login['memberVo.logonName'])

            with open(files_l[8], 'w') as f:      #将请求返回值写入到邮件附件中
                f.write(r_login.text)

            # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
            if access_hour() == 1:
                print('发送邮件和短信报警通知')
                send_mail(server, from_addr, to_addr_l, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
                sendmsg(terminal, phonenum_l, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

            else:
                print('只发送邮件发送邮件')
                send_mail(server, from_addr, to_addr_l, subject, filename=files_l[9], tt=time_f, text=text,files=[files_l[8]])  # 发送邮件

            continue     # 如果登录失败，跳出此次循环，进入下一循环

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        '''
        访问超时异常处理
        '''
        print('请求超时，用户登录失败')
        error_login_num += 1  # 登录失败次数
        with open(files_l[9], 'a') as f:  # 记录登录操作
            f.write("%s：用户【%s】登录失败，请求超时" % (time_f, params_login['memberVo.logonName']) + '\n')

        error_login = traceback.format_exc()  # 获取报错信息
        with open(files_l[8], 'w') as f:  # 将报错信息写入文件
            f.write(error_login)

        subject = '【下单监控】APP：请求超时，登录失败'
        text = "%s：请求超时，用户【%s】登录失败，详细报错见邮件附件！" % (time_f, params_login['memberVo.logonName'])

        # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
        if access_hour() == 1:
            print('发送邮件和短信报警通知')
            send_mail(server, from_addr, to_addr_l, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
            sendmsg(terminal, phonenum_l, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

        else:
            print('只发送邮件发送邮件')
            send_mail(server, from_addr, to_addr_l, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件

        continue  # 如果登录失败，跳出此次循环，进入下一循环

    except:
        '''
        所有报错都统一处理，没有细分报错。此处有可能出现的报错有：服务器拒绝的HTTPError；
        requests.exceptions.ConnectTimeout；返回值Json解析错误:
        json.decoder.JSONDecodeError
        '''
        error_login_num += 1           # 登录失败次数
        with open(files_l[9], 'a') as f:   # 记录登录操作
            f.write("%s：用户【%s】登录失败，请求异常报错" % (time_f, params_login['memberVo.logonName']) + '\n')

        error_login = traceback.format_exc()   # 获取报错信息
        with open(files_l[8], 'w') as f:   # 将报错信息写入文件
            f.write(error_login)

        subject = '【下单监控】APP：登录失败'
        text = "%s：用户【%s】登录失败，详细报错见邮件附件！"  %(time_f, params_login['memberVo.logonName'])

        # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
        if access_hour() == 1:
            print('发送邮件和短信报警通知')
            send_mail(server, from_addr, to_addr_l, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
            sendmsg(terminal, phonenum_l, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

        else:
            print('只发送邮件发送邮件')
            send_mail(server, from_addr, to_addr_l, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])

        continue      # 如果登录失败，跳出此次循环，进入下一循环


    ####################### 搜索 #############################
    try:
        time_f = time_n()  #获取当前时间
        r_search = s.post(url_search, headers=headers, data=data_search, timeout=60)
        time.sleep(random.randint(0,10))
        #print(r_search.text)
        #assert_that(r_search.text).contains('耐克' or 'NIKE' or 'Nike')  # 验证搜索结果
        assert_that(r_search.text).contains('测试商品')   # testing

        # 查询结果验证OK
        print('搜索成功')
        with open(files_l[9], 'a') as f:    # 记录搜索操作
            f.write("%s：搜索【%s】成功" % (time_f, data_search['kw']) + '\n')

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        '''
        访问超时异常处理
        '''
        print('请求超时，搜索失败')
        error_search_num += 1  # 搜索失败次数
        with open(files_l[9], 'a') as f:  # 记录搜索操作
            f.write("%s：搜索【%s】失败" % (time_f, data_search['kw']) + '\n')

        search_error = traceback.format_exc()  # 获取搜索错误信息
        with open(files_l[8], 'w') as f:  # 将异常信息写入文件，'w'模式写入信息且覆盖文件中内容
            f.write(search_error)

        subject = '【下单监控】APP：请求超时，搜索失败'
        text = "%s：请求超时，搜索【%s】失败，详细报错见邮件附件！" % (time_f, data_search['kw'])

        # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
        if access_hour() == 1:
            print('发送邮件和短信报警通知')
            send_mail(server, from_addr, to_addr_s, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
            sendmsg(terminal, phonenum_s, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

        else:
            print('只发送邮件发送邮件')
            send_mail(server, from_addr, to_addr_s, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
        time.sleep(random.randint(0, 10))

    except:
        '''
        查询失败：1、查询验证失败，报AssertError错误；2、请求访问超时报错； 3、服务器拒绝访问等
        '''
        print('搜索失败')
        error_search_num += 1           # 搜索失败次数
        with open(files_l[9], 'a') as f:    # 记录搜索操作
            f.write("%s：搜索【%s】失败" % (time_f, data_search['kw']) + '\n')

        search_error = traceback.format_exc()        # 获取搜索错误信息
        with open(files_l[8], 'w') as f:       # 将异常信息写入文件，'w'模式写入信息且覆盖文件中内容
            f.write(search_error)

        subject = '【下单监控】APP：搜索失败'
        text = "%s：搜索【%s】失败，详细报错见邮件附件！"  %(time_f, data_search['kw'])

        # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
        if access_hour() == 1:
            print('发送邮件和短信报警通知')
            send_mail(server, from_addr, to_addr_s, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
            sendmsg(terminal, phonenum_s, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

        else:
            print('只发送邮件发送邮件')
            send_mail(server, from_addr, to_addr_s, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件

        time.sleep(random.randint(0, 10))



    ################################################## 添加购物车 ##################################################
    '''
    商品添加购物车成功，返回值是：{"result":true,"errorCode":0,"errorMsg":"成功"}
    '''
    try:
        time_f = time_n()  # 获取当前时间
        r_add = s.post(url_add, headers=headers, params=params_add, timeout=60)
        time.sleep(random.randint(0,10))
        #print(r_add.json())
        r_add_j = r_add.json()

        if r_add_j['errorMsg'] == '成功' and r_add_j['errorCode'] == 0 and r_add_j['result'] == True:
            # 验证商品添加购物车成功
            print('商品添加购物车成功')

            with open(files_l[9], 'a') as f:            # 记录接口操作
                f.write("%s：商品【%s】添加购物车成功" % (time_f, params_add['goodsSku']) + '\n')

            ### 删除购物车的商品
            try:
                time_f = time_n()  # 获取当前时间
                r_delshop = s.post(url_delshop, headers=headers, data=data_delshop, timeout=60)
                time.sleep(random.randint(0, 10))
                # print('删除购物车返回值：', r_delshop.json())
                r_delshop_j = r_delshop.json()
                if r_delshop_j['errorMsg'] == '成功' and r_delshop_j['errorCode'] == 0:
                    print('购物车商品删除成功')

                    with open(files_l[9], 'a') as f:  # 记录接口操作
                        f.write("%s：商品【%s】在购物车中删除" % (time_f, data_delshop['goodsSkus']) + '\n')

                else:
                    print('购物车商品删除失败')
                    with open(files_l[9], 'a') as f:  # 记录接口操作
                        f.write("%s：商品【%s】在购物车中删除失败" % (time_f, data_delshop['goodsSkus']) + '\n')

                    subject = '【下单监控】APP：购物车商品删除失败'
                    text = "%s：商品【%s】在购物车中删除失败。\n\n1、请求返回值验证错误，返回值见邮件附件；\n\n" \
                           % (time_f, data_delshop['goodsSkus'])

                    with open(files_l[8], 'w') as f:  # 将请求返回值写入到文件中
                        f.write(r_delshop.text)

                    # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
                    if access_hour() == 1:
                        print('发送邮件和短信报警通知')
                        send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                                  files=[files_l[8]])  # 发送邮件
                        sendmsg(terminal, phonenum_a, text, time_s=time_f, filename1=files_l[9],
                                filename2=files_l[8])  # 发送短信

                    else:
                        print('只发送邮件发送邮件')
                        send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                                  files=[files_l[8]])

            except:
                print('购物车商品删除失败')
                with open(files_l[9], 'a') as f:  # 记录接口操作
                    f.write("%s：商品【%s】在购物车中删除失败" % (time_f, data_delshop['goodsSkus']) + '\n')

                delshop_error = traceback.format_exc()
                with open(files_l[8], 'w') as f:
                    f.write(delshop_error)

                subject = '【下单监控】APP：购物车商品删除失败'
                text = "%s：商品【%s】在购物车中删除失败，详细报错见邮件附件！" % (time_f, data_delshop['goodsSkus'])

                # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
                if access_hour() == 1:
                    print('发送邮件和短信报警通知')
                    send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                              files=[files_l[8]])  # 发送邮件
                    sendmsg(terminal, phonenum_a, text, time_s=time_f, filename1=files_l[9],
                            filename2=files_l[8])  # 发送短信

                else:
                    print('只发送邮件发送邮件')
                    send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                              files=[files_l[8]])
                time.sleep(random.randint(0, 10))  # 随机等待时间，防止时间限制反爬


        else:
            # 添加购物车失败：添加购物车请求返回值验证失败，发送邮件
            error_add_num += 1         # 商品添加购物车失败次数
            print('添加购物车失败')
            with open(files_l[9], 'a') as f:  # 记录登录操作
                f.write("%s：商品【%s】添加购物车失败" % (time_f, params_add['goodsSku']) + '\n')

            subject = '【下单监控】APP：商品添加购物车失败'
            text = "%s：商品【%s】添加购物车失败。\n\n请求返回值验证错误，返回值见邮件附件；" % (time_f, params_add['goodsSku'])

            with open(files_l[8], 'w') as f:    # 将请求返回值写入到文件中
                f.write(r_add.text)

            # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
            if access_hour() == 1:
                print('发送邮件和短信报警通知')
                send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                          files=[files_l[8]])  # 发送邮件
                sendmsg(terminal, phonenum_a, text, time_s=time_f, filename1=files_l[9],
                        filename2=files_l[8])  # 发送短信

            else:
                print('只发送邮件发送邮件')
                send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                          files=[files_l[8]])

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        '''
        访问超时异常处理
        '''
        print('请求超时，商品添加购物车失败')
        error_add_num += 1  # 添加购物车失败次数
        with open(files_l[9], 'a') as f:  # 记录接口操作
            f.write("%s：商品【%s】添加购物车失败" % (time_f, params_add['goodsSku']) + '\n')

        add_error = traceback.format_exc()
        with open(files_l[8], 'w') as f:
            f.write(add_error)

        subject = '【下单监控】APP：请求超时，商品添加购物车失败'
        text = "%s：请求超时，商品【%s】添加购物车失败，详细报错见邮件附件！" % (time_f, params_add['goodsSku'])

        # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
        if access_hour() == 1:
            print('发送邮件和短信报警通知')
            send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                      files=[files_l[8]])  # 发送邮件
            sendmsg(terminal, phonenum_a, text, time_s=time_f, filename1=files_l[9],
                    filename2=files_l[8])  # 发送短信

        else:
            print('只发送邮件发送邮件')
            send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                      files=[files_l[8]])
        time.sleep(random.randint(0, 10))  # 随机等待时间，防止时间限制反爬

    except:
        '''
        添加购物车失败：1、返回值Json解析失败，报json.decodeError错误；2、请求访问超时报错； 3、服务器拒绝访问等
        '''
        error_add_num += 1         # 添加购物车失败次数
        with open(files_l[9], 'a') as f:  # 记录接口操作
            f.write("%s：商品【%s】添加购物车失败" % (time_f, params_add['goodsSku']) + '\n')

        add_error = traceback.format_exc()
        with open(files_l[8], 'w') as f:
            f.write(add_error)

        subject = '【下单监控】APP：商品添加购物车失败'
        text = "%s：商品【%s】添加购物车失败，详细报错见邮件附件！" % (time_f, params_add['goodsSku'])

        # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
        if access_hour() == 1:
            print('发送邮件和短信报警通知')
            send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                      files=[files_l[8]])  # 发送邮件
            sendmsg(terminal, phonenum_a, text, time_s=time_f, filename1=files_l[9],
                    filename2=files_l[8])  # 发送短信

        else:
            print('只发送邮件发送邮件')
            send_mail(server, from_addr, to_addr_a, subject, filename=files_l[9], tt=time_f, text=text,
                      files=[files_l[8]])
        time.sleep(random.randint(0, 10))  # 随机等待时间，防止时间限制反爬

    ############################################### 提交订单 ########################################################
    '''
    提交订单成功，返回值是：
    {"result":true,"errorCode":0,"errorMsg":"成功","orderId":7417638,"orderNo":"2110176173819",
    "leftAmount":"0.01","paySuccessUrl":"","uploadIdCardStatus":true,"paySuccessStatus":false}
    '''
    try:
        time_f = time_n()  # 获取生成订单的时间
        r_submit = s.post(url_submit, headers=headers, data=data_submit, timeout=60)
        time.sleep(random.randint(0,10))

        # print('提交订单返回值：%s' %(r_submit.json()))
        r_submit_j = r_submit.json()      # 将返回响应通过json解析成python数据
        print('json返回值类型：%s' %(type(r_submit_j)))


        if r_submit_j['errorCode'] == 0 and r_submit_j['errorMsg'] == '成功' and r_submit_j['orderNo'] != "":
            # 订单创建成功
            print('订单：%s创建成功' %(r_submit_j['orderNo']))
            with open(files_l[9], 'a') as f:     # 将创建的订单记录到文件中
                f.write("%s：订单【%s】创建成功" %(time_f, r_submit_j['orderNo']) + '\n')

            ################# 取消订单 ##################
            try:
                time_f = time_n()         # 获取当前时间
                params_cancel['cancelVo.orderId'] = r_submit_j['orderId']   # 获取取消订单参数
                r_cancel = s.post(url_cancel, headers=headers, params=params_cancel, timeout=60)  # 取消订单
                time.sleep(random.randint(0, 10))

                if r_cancel.json()['errorCode'] == 0 and r_cancel.json()['errorMsg'] == '成功':
                    print('订单：%s 取消成功' %(r_submit_j['orderNo']))
                    with open(files_l[9], 'a') as f:            # 记录操作
                        f.write("%s：订单【%s】取消成功" %(time_f, r_submit_j['orderNo']) + '\n')
                else:
                    print('订单取消失败')
                    with open(files_l[9], 'a') as f:    # 记录操作
                        f.write("%s：订单【%s】取消失败" %(time_f, r_submit_j['orderNo']) + '\n')

                    subject = "【下单监控】APP：订单取消失败"
                    text = "%s：订单【%s】取消失败。\n\n请求返回值验证错误，返回值见邮件附件" %(time_f, r_submit_j['orderNo'])

                    with open(files_l[8], 'w') as f:
                        f.write(r_cancel.text)

                    # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
                    if access_hour() == 1:
                        print('发送邮件和短信报警通知')
                        send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                                  files=[files_l[8]])  # 发送邮件
                        sendmsg(terminal, phonenum_o, text, time_s=time_f, filename1=files_l[9],
                                filename2=files_l[8])  # 发送短信

                    else:
                        print('只发送邮件发送邮件')
                        send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                                  files=[files_l[8]])

            except:
                print('订单取消失败')
                with open(files_l[9], 'a') as f:  # 记录操作
                    f.write("%s：订单【%s】取消失败" % (time_f, r_submit_j['orderNo']) + '\n')

                cancel_error = traceback.format_exc()
                with open(files_l[8], 'w') as f:
                    f.write(cancel_error)

                subject = "【下单监控】APP：订单取消失败"
                text = "%s：订单【%s】取消失败，错误信息见邮件附件。" % (time_f, r_submit_j['orderNo'])

                # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
                if access_hour() == 1:
                    print('发送邮件和短信报警通知')
                    send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                              files=[files_l[8]])  # 发送邮件
                    sendmsg(terminal, phonenum_o, text, time_s=time_f, filename1=files_l[9],
                            filename2=files_l[8])  # 发送短信

                else:
                    print('只发送邮件发送邮件')
                    send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                              files=[files_l[8]])


            ################### 删除订单 ####################
            try:
                time_f = time_n()           # 获取当前时间
                params_delete['orderId'] = r_submit_j['orderId']      # 获取删除订单参数
                r_delete = s.post(url_delete, headers=headers, params=params_delete, timeout=60)
                time.sleep(random.randint(0, 10))

                if r_delete.json()['errorCode'] == 0 and r_delete.json()['errorMsg'] == '成功':
                    # 订单删除成功
                    print('订单：%s 删除成功' %(r_submit_j['orderNo']))
                    with open(files_l[9], 'a') as f:      # 将删除的订单记录到文件中
                        f.write('%s：订单【%s】删除成功' %(time_f, r_submit_j['orderNo']) + '\n\n')

                else:
                    with open(files_l[9], 'a') as f:
                        f.write("%s：订单【%s】删除失败" %(time_f, r_submit_j['orderNo']) + '\n\n')

                    subject = "【下单监控】APP：订单删除失败"
                    text = "%s：订单【%s】删除失败。\n\n请求返回值验证错误，返回值见邮件附件" % (time_f, r_submit_j['orderNo'])

                    with open(files_l[8], 'w') as f:               # 将请求返回值写入到邮件附件中
                        f.write(r_delete.text)

                    # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
                    if access_hour() == 1:
                        print('发送邮件和短信报警通知')
                        send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                                  files=[files_l[8]])  # 发送邮件
                        sendmsg(terminal, phonenum_o, text, time_s=time_f, filename1=files_l[9],
                                filename2=files_l[8])  # 发送短信

                    else:
                        print('只发送邮件发送邮件')
                        send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                                  files=[files_l[8]])

            except:
                with open(files_l[9], 'a') as f:  # 记录操作
                    f.write("%s：订单【%s】删除失败" % (time_f, r_submit_j['orderNo']) + '\n\n')

                delete_error = traceback.format_exc()    # 获取错误信息
                with open(files_l[8], 'w') as f:        # 将错误信息写入文件中
                    f.write(delete_error)

                subject = "【下单监控】APP：订单删除失败"
                text = "%s：订单【%s】删除失败，错误信息见邮件附件。" % (time_f, r_submit_j['orderNo'])

                # --------------发送报警通知，access_hour()为1时发送邮件和短信报警，否则只发送邮件
                if access_hour() == 1:
                    print('发送邮件和短信报警通知')
                    send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                              files=[files_l[8]])  # 发送邮件
                    sendmsg(terminal, phonenum_o, text, time_s=time_f, filename1=files_l[9],
                            filename2=files_l[8])  # 发送短信

                else:
                    print('只发送邮件发送邮件')
                    send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text,
                              files=[files_l[8]])

        # 订单创建失败
        else:
            # 提交订单失败：提交订单请求返回值验证失败，发送邮件
            print('订单创建失败')
            with open(files_l[9], 'a') as f:     # 记录操作：提交订单失败
                f.write("%s：订单创建失败" % time_f + '\n\n')

            error_submit_num += 1
            text = "%s：订单提交失败。\n\n请求返回值验证错误，返回值见邮件附件；" % time_f
            subject = '【下单监控】APP：订单提交失败'

            with open(files_l[8], 'w') as f:
                f.write(r_submit.text)

            send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
            sendmsg(terminal, phonenum_o, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        '''
        访问超时异常处理
        '''
        print('请求超时，订单创建失败')
        with open(files_l[9], 'a') as f:  # 记录操作：提交订单失败
            f.write("%s：订单创建失败" % time_f + '\n\n')

        error_submit_num += 1
        submit_error = traceback.format_exc()
        with open(files_l[8], 'w') as f:
            f.write(submit_error)

        time_f = time_n()
        text = "%s：请求超时，订单提交失败, 错误信息见邮件附件，谢谢！\n\n" % time_f
        subject = '【下单监控】APP：请求超时，订单提交失败'

        send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
        sendmsg(terminal, phonenum_o, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

    except:
        '''
        创建订单失败：1、返回值Json解析失败，报json.decodeError错误；2、请求访问超时报错； 3、服务器拒绝访问等
        '''
        print('订单创建失败')
        with open(files_l[9], 'a') as f:  # 记录操作：提交订单失败
            f.write("%s：订单创建失败" % time_f + '\n\n')

        error_submit_num += 1
        submit_error = traceback.format_exc()
        with open(files_l[8], 'w') as f:
            f.write(submit_error)

        time_f = time_n()
        text = "%s：订单提交失败, 错误信息见邮件附件，谢谢！"  % time_f
        subject = '【下单监控】APP：订单提交失败'

        send_mail(server, from_addr, to_addr_o, subject, filename=files_l[9], tt=time_f, text=text, files=[files_l[8]])  # 发送邮件
        sendmsg(terminal, phonenum_o, text, time_s=time_f, filename1=files_l[9], filename2=files_l[8])  # 发送短信

    s.close()  # 关闭会话

    time_2 = time.time()          # 记录循环结束时间
    time_r = int(time_2) - int(time_1)  # 一个循环运行总时间
    print('程序运行时间：%s 秒' % time_r)
