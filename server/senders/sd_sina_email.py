# coding: utf-8
# sayheya@qq.com
# 2019-05-29
import time
import traceback
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from senders.base_sender import BaseSender
from config import SINA_SMTP_USER, SINA_SMTP_PASS, SINA_SMTP_RECEIVERS


class SinaSmtpSender(BaseSender):
    name = 'SinaEmail'

    def __init__(self, *args, **kwargs):
        self.user = self.decode_base64(SINA_SMTP_USER)
        self.passwd = self.decode_base64(SINA_SMTP_PASS)
        self.receivers = [self.decode_base64(i) for i in SINA_SMTP_RECEIVERS]
        super(SinaSmtpSender, self).__init__(*args, **kwargs)

    def smtp_sendmail(self, subject, mail_content):
        """SMTP 邮件发送模块

        :param mail_host:   设置服务器
        :param mail_user:   用户名
        :param mail_pass:   口令
        :param receivers:   接收邮件者，可设置为你的QQ邮箱或者其他邮箱，可传入一个邮箱list
        :param name_sender:   设置发件人名称
        :param name_receiver:   设置收件人名称
        :param subject:   设置邮件主题
        :param mail_content:   设置邮件内容
        :return:   无
        """

        # # 第三方 SMTP 服务 （默认配置信息设置区）
        mail_host = "smtp.sina.com"  # 设置服务器
        mail_user = self.user  # 用户名
        mail_pass = self.passwd  # 口令
        receivers = self.receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱，可传入一个邮箱list

        name_sender = "MailRobot"  # 设置发件人名称
        name_receiver = "Admin"  # 设置收件人名称

        # 考虑到编码的原因，这里统一将name属性值改成utf-8，地址的话一定是统一的邮箱地址结构，所以不考虑
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        # 功能区
        message = MIMEText(mail_content, 'html', 'utf-8')
        message['From'] = _format_addr('%s <%s>' % (name_sender, mail_user))
        # message['From'] = formataddr((Header('测试', 'utf-8').encode(),mail_user))
        message['To'] = _format_addr('%s <%s>' % (name_receiver, receivers))
        message['Subject'] = Header(subject, 'utf-8')

        # print(message)

        # 发送区
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 25 为 SMTP 端口号
            # smtpObj.set_debuglevel(1)  # 调试显示邮件发送交互信息
            # smtpObj.starttls()
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(mail_user, receivers, message.as_string())
            smtpObj.quit()
            self.logger.info("has send the mail to {}.".format(' '.join(receivers)))
        except:
            self.logger.error("send error！\nerror: " + str(traceback.format_exc()))

    def send(self, title, content):
        pass


if __name__ == '__main__':
    pass
