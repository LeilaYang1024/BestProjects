# coding: utf-8

"""
Created on:
@brief:python SMTP 邮件发送
@author: YangLei
@version: Python3
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header


class SendMails(object):
    mail_host = "smtp.163.com"      # 设置服务器
    mail_user = "kba_data@163.com"  # 用户名
    mail_pass = "FUTEUGWCVGJSMIEP"  # 口令(邮箱开启STMP拿到的客户端授权码)
    sender = "kba_data@163.com"     # 发件人邮箱

    def __init__(self,receivers):
        """
        添加收件人
        :param receivers: list,支持多个收件人
        """
        self.receivers=receivers


    def mail_file(self,filename):
        """
        构造邮件附件,MIMEApplication支持excel表格，文档，图片等各种附件形式
        :return:
        """
        att = MIMEApplication(open(filename, "rb").read())
        att.add_header("Content-Disposition", "attachment", filename=filename)
        return att

    def mail_message(self,type,subject,content,files=None):
        """
        构造邮件内容
        :param type: 邮件内容类型，file->带附件,text->普通文本，html->html片段
        :param subject: 邮件主题
        :param content: 邮件正文内容
        :return:
        """
        if type=='file':
            message=MIMEMultipart()
            message.attach(MIMEText(content, 'plain', 'utf-8'))
            for file in files:
                att=self.mail_file(file)
                message.attach(att)
        elif type=='html':
            message=MIMEText(content, 'html', 'utf-8')
        else:
            message=MIMEText(content, 'plain', 'utf-8')
        message['To'] = ','.join(self.receivers)  # 收件人
        message['From'] = self.sender  # 发件人
        message['Subject'] = Header(subject, 'utf-8')
        return message

    def send_mail(self,message):
        try:
            #使用SSL发送邮件，部署服务器必须使用该方式
            smtpObj = smtplib.SMTP_SSL(self.mail_host)

            #使用普通的方式发送邮件
            #smtpObj = smtplib.SMTP()
            #smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号

            smtpObj.login('kba_data@163.com', self.mail_pass)
            smtpObj.sendmail(self.sender,self.receivers, message.as_string())
            print('邮件发送成功')
        except:
            print('邮件发送失败')


if __name__=="__main__":
    receivers=['yanglei@kanda-data.com']
    a=SendMails(receivers).mail_message(type='text',subject='这是一份监控测试邮件',content='您好')
    SendMails(receivers).send_mail(message=a)


