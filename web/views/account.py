import smtplib
from django import forms
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse

from email.mime.text import MIMEText
from email.header import Header
from utils.encrypt import md5
from web import models


class LoginForm(forms.Form):
    role = forms.ChoiceField(label='角色', choices=(('1', '管理员'), ('2', '客户')), widget=forms.Select(attrs={
        'class': 'form-control'}))
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'},
                                                          render_value=type))

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            from django.core.exceptions import ValidationError
            raise ValidationError('用户名格式错误')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) > 8:
            from django.core.exceptions import ValidationError
            raise ValidationError('密码格式错误')
        return password

    def clean(self):
        print(self.cleaned_data)
        # from django.core.exceptions import ValidationError
        # raise ValidationError('整体错误')


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        print('验证失败')
        return render(request, 'login.html', {'form': form})
    role = form.cleaned_data.get('role')
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    # if password:
    password = md5(password)
    if role == '1':
        user_object = models.Administrator.objects.filter(active=1, username=username, password=password).first()
    else:
        user_object = models.Customer.objects.filter(active=1, username=username, password=password).first()
    if not user_object:
        return render(request, 'login.html', {'error': '用户名或密码错误', 'form': form})
    return HttpResponse('登陆成功')


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
        server.login(sender, email_password)  # 登录邮箱账号
        server.sendmail(sender, receiver, msg.as_string())  # 发送邮件
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"邮件发送失败: {e}")
    finally:
        server.quit()  # 关闭连接


class SmsloginForm(forms.Form):
    role = forms.ChoiceField(label='角色', choices=(('1', '管理员'), ('2', '客户')), widget=forms.Select(attrs={
        'class': 'form-control'}))
    mobile = forms.CharField(label='手机号',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手机号'}))
    code = forms.CharField(label='短信验证码',
                           validators=[RegexValidator(r'^[1-9]+$', "验证码必须为数字"), ],  # 正则表达式
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '短信验证码'}))

def sms_login(request):
    if request.method == 'GET':
        form = SmsloginForm()
        return render(request, 'sms_login.html', {'form': form})
