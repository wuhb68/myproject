import smtplib
from django import forms
from django.shortcuts import render, HttpResponse

from email.mime.text import MIMEText
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




def sms_login(request):
    send_163_email(
        sender='haibin681528@163.com',  # 你的163邮箱地址
        auth_code='JXyAZP9w927KayLL',  # 你的SMTP授权码
        receiver='1071794363@qq.com',  # 收件人邮箱
        subject='欢迎登录',
        content='您的邮箱验证码为123456\n\n1分钟内有效!'
    )
    return render(request, 'sms_login.html')
