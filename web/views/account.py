import smtplib
import random
from django import forms
from django.core.validators import RegexValidator
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django_redis import get_redis_connection
from email.mime.text import MIMEText
from email.header import Header

from matplotlib.font_manager import json_dump

from utils.encrypt import md5
from utils.tencent import send_163_email
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


class SmsloginForm(forms.Form):
    role = forms.ChoiceField(label='角色', choices=(('1', '管理员'), ('2', '客户')), widget=forms.Select(attrs={
        'class': 'form-control'}))
    mobile = forms.CharField(label='手机号',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手机号'}))
    code = forms.CharField(label='短信验证码',
                           validators=[RegexValidator(r'^[1-9]+$', "验证码必须是数字"), ],  # 正则表达式
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '短信验证码'}))


def sms_login(request):
    if request.method == 'GET':
        form = SmsloginForm()
        return render(request, 'sms_login.html', {'form': form})


class MobileForm(forms.Form):
    mobile = forms.CharField(label='手机号', required=True,
                             validators=[RegexValidator(r'^1\d{10}', '手机号格式错误'), ])


def sms_send(request):
    """发送短信"""
    # 1. 校验手机号格式
    request.POST.get('mobile')
    form = MobileForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse({'status': False, 'detail': form.errors}, json_dumps_params={"ensure_ascii": False})

    # 2. 发送短信生成验证码
    mobile = form.cleaned_data.get('mobile')
    sms_code = random.randint(1000, 9999)
    is_success = send_163_email(mobile, str(sms_code))
    if not is_success:
        return JsonResponse({'status':False,"detail":{'mobile':["发送失败,请稍等重试"]}},json_dumps_params={"ensure_ascii": False})

    # 3. 保存手机号验证码，便于下次校验
    return HttpResponse('成功')
