import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_163_email(mobile, sms_code):
    sender = 'haibin681528@163.com'
    receiver = '1071794363@qq.com'
    # 邮箱账号和密码（注意：这里的密码不是登录密码，而是授权码）
    email_password = 'LJu4nAW2EKjeJ36r'  # 这是授权码，不是登录密码
    subject = '欢迎登录'
    content = f'你的手机号{mobile}，验证码为{sms_code}，1分钟内有效'
    # 邮件内容
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    # 网易邮箱的SMTP服务器地址和端口
    smtp_server = 'smtp.163.com'
    smtp_port = 465  # 或者使用25/587，取决于你的服务器配置和安全性需求

    try:
        # 创建SMTP对象并连接到服务器
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用SSL连接（推荐）
        server.login(sender, email_password)  # 登录邮箱账号
        server.sendmail(sender, receiver, msg.as_string())  # 发送邮件
        print("邮件发送成功")
        return True
    except smtplib.SMTPException as e:
        print(f"邮件发送失败: {e}")
        return False
    finally:
        server.quit()  # 关闭连接


if __name__ == '__main__':
    send_163_email('18659542543','2543')
