from django.shortcuts import render, HttpResponse
from web import models
from utils.encrypt import md5
from django import forms


class LoginForm(forms.Form):
    role = forms.ChoiceField(label='角色', choices=(('1', '管理员'), ('2', '客户')), widget=forms.Select(attrs={
        'class': 'form-control'}))
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'},
                                                          render_value=type))

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {'form': form})
    role = form.cleaned_data['role']
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    # role = request.POST.get('role')
    # username = request.POST.get('username')
    # password = request.POST.get('password')
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
