from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect


class UserInfo(object):
    def __init__(self, role, name, id):
        self.role = role
        self.name = name
        self.id = id

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """校验用户是否已登录"""
        # 1.不需要登录就能访问的URL
        if request.path_info in settings.NB_WHITE_URL:     #request.path_info指当前用户访问的url
            return
        # session中获取用户信息，能获取到登录成功;未登录
        user_dict = request.session.get(settings.NB_SESSION_KEY)
        # # {'role': mapping[role], 'name': user_object.username,'id': user_object.id}
        # 未登录，跳转回登录页面
        if not user_dict:
            return redirect(settings.NB_LOGIN_URL)
        # 已登录封装用户信息
        request.nb_user = UserInfo(**user_dict)
        print(request.nb_user.name)

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass
    # def process_response(self, request, response):
    #     pass