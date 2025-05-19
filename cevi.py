import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_163_email(sender, auth_code, receiver, subject, content):
    # 设置邮件内容
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(('发件人昵称', sender))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(('收件人昵称', receiver))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = subject  # 邮件的主题

    try:
        # 163邮箱的SMTP服务器地址和端口
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.login(sender, auth_code)  # 登录邮箱
        server.sendmail(sender, [receiver], msg.as_string())  # 发送邮件
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")


# 使用示例
send_163_email(
    sender='haibin681528@163.com',  # 你的163邮箱地址
    auth_code='JXyAZP9w927KayLL',  # 你的SMTP授权码
    receiver='1071794363@qq.com',  # 收件人邮箱
    subject='欢迎登录',
    content='您的手机号验证码为123456\n\n1分钟内有效!'
)