from django import forms
from django.shortcuts import render, HttpResponse

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
        print('验证失败!')
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


def sms_login(request):
    return render(request, 'sms_login.html')
