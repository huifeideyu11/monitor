import os
from smtplib import SMTP
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE,formatdate
from email.header import Header
from email import encoders
import time, requests

def time_c():
    # 获取当前时间，以str类型返回前13位数字
    # 获取当前时间，以str类型返回前13位数字
    time_now = str(time.time())
    time_str = time_now.split('.')[0] + time_now.split('.')[1]
    return time_str[0:13]

def time_n():
    '''
    获取当前时间，并格式化
    :return: 返回格式化后的时间格式
    '''
    time_f = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time_f

def access_hour():
    '''
       获取当前时间的小时数
       参数：
            start_time：起始时间
            end_time:终止时间
       :return: 在起始时间和终止时间内，返回值：0； 否则返回：1
    '''
    time_h = time.localtime(time.time())[3]   # 获取当前时间的小时值
    if 0 <= time_h <= 7:
        return 0
    else:
        return 1


def send_mail(server, from_addr, to_addr, subject, filename='', tt='', text="", files=[]):
    '''
    邮件发送函数
    :param server:是一个字典，包括用户名，密码，邮箱Host和端口号
    :param from_addr: 邮件发送者：char
    :param to_addr: 邮件接受者：list——由邮件接收者组成的列表,可以群发邮件
    :param msg: 邮件内容
    :param text:默认为空，为字符串类型的文本内容
    :param files:当有附件添加时使用该参数，无附件时默认为空。files可以是图片，txt文本内容、影视频；
    :param filename:文件路径+名称
    :param tt：时间
    :return: 无
    注：from_addr为邮箱发送者，但是在msg中可以设置邮件接收者显示的发送
    '''
    msg = MIMEMultipart()
    msg['Subject'] = subject           # 邮件主题
    # msg['From'] = '邮件发送者'             # 此处可以设置邮件发送者，但并不一定是真正的邮件发送者

    try:
        msg_text = MIMEText(text, 'plain', 'utf-8')
        msg.attach(msg_text)             # 将文本信息添加到邮件主体中

        for file in files:              # 添加附件
            msg_base = MIMEBase('application', 'octet-stream')
            with open(file, 'rb') as f:
                msg_base.set_payload(f.read())         # 将文件的内容写入邮件信息中
            encoders.encode_base64(msg_base)           # 编译msg_base
            msg_base.add_header('Content-Disposition', 'attachment', filename="%s" % os.path.basename(file))
            msg.attach(msg_base)

        smtp = SMTP(server['host'], server['port'])                   # 连接smtp发件箱的服务器
        smtp.login(server['username'], server['psw'])          # 登录邮箱
        smtp.sendmail(from_addr, to_addr, msg.as_string())      # 发送邮件
        smtp.close()             # 关闭邮箱
        with open(filename, 'a') as f:   # 将短信发送失败记录写入操作记录文件中
            f.write('{}：邮件发送成功'.format(tt) + '\n')
        print('邮件发送成功')

    except:
        '''
        此处未做短信发送异常处理。邮件发送失败，短信也发送失败的概率比较小
        '''

        tel = '13694917391'    # 多个号码中间用逗号隔开，但是不留空格, tel为str类型，不可为空
        lenth = len(tel.split(','))
        msg = '下单监控异常，且邮件发送失败。错误类型：' + text
        url = 'http://ws.montnets.com:9002/MWGate/wmgw.asmx/MongateCsSpSendSmsNew?' \
              'userId=J30173&password=080056&pszMobis={0}&pszMsg={1}&iMobiCount={2}&' \
              'pszSubPort=106571014054499'.format(tel, msg, lenth)

        r = requests.get(url, timeout=30)
        print('短信通知：邮件发送失败')
        with open(filename, 'a') as f:  # 将短信发送失败记录写入操作记录文件中
            f.write('{}：邮件发送失败，短信提醒'.format(tt) + '\n')


if __name__ == "__main__":
    '''
    server = {'username':'yongsheng.luo@xiu.com', 'psw':'19910204514liu', 'host':"smtp.xiu.com", 'port':25}
    from_addr = 'yongsheng.luo@xiu.com'
    to_addr = ['631442624@qq.com', 'yongsheng.luo@xiu.com']
    subject = '下单异常'
    text = "测试邮件"
    files = ['D:\luotian\Pycharm_Project\InterFace_test\Error_report\无线项目.png',
             'D:\luotian\Pycharm_Project\InterFace_test\Error_report\测试附件1.txt']
    send_mail(server, from_addr, to_addr, subject, text, files)
    print('邮件发送成功')
    '''
    print(access_hour())