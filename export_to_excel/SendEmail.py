# coding: utf-8
#
# 发送邮件模块
#
#

import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendEmail:
    """
    可发送带附件的邮件或者普通邮件
    """

    def __init__(self, smtp_server, port, user, passwd, ssl, sender, receivers, subject,
                 content_path, attach_files=None, attach_title=None, *kw, **kwargs):
        """
        :param smtp_server: 发送邮件服务器
        :param port: 服务端口
        :param user: 登陆账号
        :param passwd: 密码
        :param ssl: 是否启用方式
        :param sender:发送方
        :param receivers:接收邮件列表
        :param subject:邮件主题
        :param content_path:正文文件路径
        :param attach_files:附件列表
        :param attach_title:附件名称
        """
        self.smtp_server = smtp_server
        self.port = port
        self.user = user
        self.passwd = passwd
        self.ssl = ssl
        self.From = sender
        self.To = receivers
        self.subject = subject
        self.attach_files = attach_files
        self.content_path = content_path
        self.attach_title = attach_title

    def send(self):
        # 邮件发送，接收及主题
        multipart = MIMEMultipart()
        multipart['From'] = self.From
        multipart['To'] = ','.join(self.To)
        multipart['Subject'] = Header(self.subject, "utf-8")

        # 判断邮件正文文件是否存在
        if os.path.isfile(self.content_path):
            content_path = MIMEText(_text=open(self.content_path, 'rb').read(), _subtype='html', _charset='utf-8')
            multipart.attach(content_path)
        else:
            raise IOError("content path is not exists!")

        # 判断附件是否存在
        if isinstance(self.attach_files, list):
            for attach in self.attach_files:
                if not os.path.exists(attach):
                    raise IOError("attach file is not exists")

        # 添加附件
        for attach in self.attach_files:
            if self.attach_title=='':
                _,attach_name = os.path.split(attach)
            else:
                attach_name = self.attach_title

            attach = MIMEText(open(attach, 'rb').read(), 'base64', 'utf-8')
            attach['Content-Type'] = 'application/octet-stream'
            # attach['Content-Disposition'] = 'attachment; filename=%s' % self.attach_title
            # attach['Content-Disposition'] = 'attachment;filename=attach'

            attach.add_header('Content-Disposition', 'attachment', filename=attach_name)
            multipart.attach(attach)

        # 是否启用安全连接
        if self.ssl:
            smtp = smtplib.SMTP_SSL(host=self.smtp_server, port=self.port)
        else:
            smtp = smtplib.SMTP(host=self.smtp_server, port=self.port)

        # 尝试发送
        try:
            smtp.login(self.user, self.passwd)
            smtp.sendmail(self.From, self.To, multipart.as_string())
        except smtplib.SMTPConnectError as e:
            print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print('邮件发送失败, ', e.message)
        except Exception as e:
            print('邮件发送异常, ', str(e))
        finally:
            smtp.quit()


def main():
    send_info = {
        'smtp_server': '',   # 邮箱的smtp地址
        'port': 25,   # 邮箱端口
        'user': '',  # 邮箱
        'passwd': '',   # 邮箱密码
        'ssl': False,
        'sender': '',  # 发送邮件
        'receivers': ['', ],   # 接收者邮箱列表
        'subject': 'cachecloud初始化脚本',
        'content_path': '',   # 邮件内容所在的文本路径
        'attach_files': [''], # 附件列表
        'attach_title': ''  # 附件的标题，如果为空则使用附件的名称
    }
    sendemail = SendEmail(**send_info)
    sendemail.send()


if __name__ == '__main__':
    main()

