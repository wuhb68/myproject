# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.header import Header
#
#
# def send_163_email(sender, password, receiver, subject, content, smtp_server='smtp.163.com', port=25):
#     """
#     使用163邮箱发送邮件
#
#     参数:
#         sender (str): 发件人邮箱地址
#         password (str): 发件人邮箱密码或授权码
#         receiver (str or list): 收件人邮箱地址，可以是字符串或列表
#         subject (str): 邮件主题
#         content (str): 邮件正文内容
#         smtp_server (str): SMTP服务器地址，默认为smtp.163.com
#         port (int): SMTP服务器端口，默认为25(也可以使用465或994 SSL端口)
#     """
#     try:
#         # 创建邮件对象
#         message = MIMEMultipart()
#         message['From'] = Header(sender, 'utf-8')
#         message['Subject'] = Header(subject, 'utf-8')
#
#         # 如果收件人是列表，转换为逗号分隔的字符串
#         if isinstance(receiver, list):
#             message['To'] = Header(','.join(receiver), 'utf-8')
#         else:
#             message['To'] = Header(receiver, 'utf-8')
#
#         # 添加邮件正文
#         message.attach(MIMEText(content, 'plain', 'utf-8'))
#
#         # 连接SMTP服务器
#         if port == 465:
#             # SSL加密方式
#             server = smtplib.SMTP_SSL(smtp_server, port)
#         else:
#             server = smtplib.SMTP(smtp_server, port)
#             if port == 25:
#                 # 非SSL加密方式，需要手动开启TLS
#                 server.starttls()
#
#         # 登录SMTP服务器
#         server.login(sender, password)
#
#         # 发送邮件
#         server.sendmail(sender, receiver, message.as_string())
#
#         # 关闭连接
#         server.quit()
#         print("邮件发送成功")
#         return True
#     except Exception as e:
#         print(f"邮件发送失败: {e}")
#         return False
#
#
# # 使用示例
# if __name__ == '__main__':
#     # 发件人邮箱（需要开启SMTP服务）
#     sender = 'haibin681528@163.com'
#     # 邮箱密码或授权码（建议使用授权码）
#     password = 'LJu4nAW2EKjeJ36r'
#     # 收件人邮箱
#     receiver = '1071794363@qq.com'
#     # 邮件主题
#     subject = 'Python邮件测试'
#     # 邮件内容
#     content = '这是一封来自Python的测试邮件。'
#
#     # 发送邮件
#     send_163_email(sender, password, receiver, subject, content)


import smtplib
from email.mime.text import MIMEText
from email.header import Header

# # 发送者和接收者的邮箱地址
# sender = 'haibin681528@163.com'
# receiver = '1071794363@qq.com'
#
# # 邮箱账号和密码（注意：这里的密码不是登录密码，而是授权码）
# email_account = 'haibin681528@163.com'
# email_password = 'LJu4nAW2EKjeJ36r'  # 这是授权码，不是登录密码
#
# # 邮件内容
# msg = MIMEText(f'您的邮箱验证码为123456\n\n1分钟内有效!', 'plain', 'utf-8')
# msg['Subject'] = Header('欢迎登录', 'utf-8')
# msg['From'] = sender
# msg['To'] = receiver
#
# # 网易邮箱的SMTP服务器地址和端口
# smtp_server = 'smtp.163.com'
# smtp_port = 465  # 或者使用25/587，取决于你的服务器配置和安全性需求
#
# try:
#     # 创建SMTP对象并连接到服务器
#     server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用SSL连接（推荐）
#     # server = smtplib.SMTP(smtp_server, smtp_port)  # 如果使用非SSL连接，取消上面的注释，并注释掉这行
#     # server.starttls()  # 如果使用非SSL连接，取消上面的注释，并取消这行的注释
#     server.login(sender, email_password)  # 登录邮箱账号
#     server.sendmail(sender, receiver, msg.as_string())  # 发送邮件
#     print("邮件发送成功")
# except smtplib.SMTPException as e:
#     print(f"邮件发送失败: {e}")
# finally:
#     server.quit()  # 关闭连接

def send_163_email(subject, content):
    sender = 'haibin681528@163.com'
    receiver = '1071794363@qq.com'

    # 邮箱账号和密码（注意：这里的密码不是登录密码，而是授权码）
    email_password = 'LJu4nAW2EKjeJ36r'  # 这是授权码，不是登录密码

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
        # server = smtplib.SMTP(smtp_server, smtp_port)  # 如果使用非SSL连接，取消上面的注释，并注释掉这行
        # server.starttls()  # 如果使用非SSL连接，取消上面的注释，并取消这行的注释
        server.login(sender, email_password)  # 登录邮箱账号
        server.sendmail(sender, receiver, msg.as_string())  # 发送邮件
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"邮件发送失败: {e}")
    finally:
        server.quit()  # 关闭连接




if __name__ == '__main__':
    send_163_email(
        subject='欢迎登录',
        content='您的邮箱验证码为123456\n\n1分钟内有效!'
    )