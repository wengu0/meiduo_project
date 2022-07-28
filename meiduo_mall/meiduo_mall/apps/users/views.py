from django import http
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
import re
from users.models import User
from django.db import DatabaseError
# Create your views here.

class RegisterView(View):
    """用户注册"""
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        """实现用户注册业务逻辑"""
        # 接受参数，表单数据

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        # 检验参数， 前后端校验需要分开，避免恶意用户越过前端逻辑要相同
        # 判断参数是否齐全
        # 判断参数是否齐全all([列表]): 会去检验列表中的元素是否为空，只要为空返回false
        if not all([username,password,password2,mobile,allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[A-Za-z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个字符
        if not re.match(r'^[A-Za-z0-9]{8,20}$',password):
            return http.HttpResponseForbidden('请输入8-20个字符的密码')
        # 判断两次输入的密码是否一致
        if password!=password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号码是否合法
        if not re.match(r'1[3-9]\d{9}',mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 判断用户是否勾选了协议
        if allow !='on':
            return http.HttpResponseForbidden('请勾选用户协议')

        # 保存注册数据
        try:
            User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            return render(request,'register.html',{'register_errmsg':'注册失败'})

        # 响应结果
        # return http.HttpResponseForbidden('注册成功，首页')
        # return  redirect('/')
        return redirect(reverse('contents:index'))