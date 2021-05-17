
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import configparser as cparser
from autodemo.config.public_data import *
from log import my_log

# --------- 读取config.ini配置文件 ---------------
cf = cparser.ConfigParser()
cf.read("../config/config.ini", encoding='UTF-8')
send_user = cf.get("mail", "send_user")
password = cf.get("mail", "password")
receive = cf.get("mail", "receive")
subject = cf.get("mail", "subject")
server_address = cf.get("mail", "server_address")


class Email:
    logger = my_log.Logger('../log/log/all.log', level='debug').logger

    def sendemail(self):
        # 测试文件
        file = '../report/测试报告.html'

        if os.path.exists(file):
            # 内容
            email_text = "测试完成！测试报告已生成，请查看附件 ~ "
            # 构造邮件体
            msg = MIMEMultipart()
            msg['subject'] = subject  # 主题
            msg['from'] = send_user  # 发送邮箱
            msg['to'] = receive  # 接收邮箱
            # 构建正文
            part_text = MIMEText(email_text)
            msg.attach(part_text)  # 正文添加到邮件体中
            # 构造附件1
            att1 = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="TestReport.html"'
            msg.attach(att1)

            # #构建附件2
            # part_attach1 = MIMEApplication(open(file,'rb').read())
            # part_attach1.add_header('Conten-Disposition','attachment',filename="testReport.html")
            # msg.attach(part_attach1)        #附件添加到邮件体中

            try:
                # 发送邮件
                smtp = smtplib.SMTP_SSL(server_address, 465)  # 启用SSL发信, 端口一般是465
                smtp.login(send_user, password)  # 登录验证
                smtp.sendmail(send_user, receive, msg.as_string())  # 发送
                self.logger.info("测试结果邮件发送成功~")
            except smtplib.SMTPException as e:
                self.logger.error("发送测试结果邮件失败！", e)
        else:
            self.logger.warning("没有找到[../report/测试报告.html]这个文件～")


if __name__ == "__main__":
    Email().sendemail()
