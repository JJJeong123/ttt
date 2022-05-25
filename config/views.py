import json
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin

import pandas as pd
import numpy as np
import mlxtend
from mlxtend.frequent_patterns import fpgrowth, association_rules, apriori
from mlxtend.preprocessing import TransactionEncoder
import openpyxl

from config.models import Member, Membership, Product, CartProduct

class index(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        if request.user.is_authenticated:
            context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
            context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        bestid = best()

        shop = Product.objects.filter(shop_id=13)
        bestset = Product.objects.filter(id__in=bestid)

        context['shop'] = shop
        context['bestset'] = bestset

        return render(request, 'index.html', context)

class LoginView(View):
    '''
    로그인 기능
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        #이미 로그인한 상태
        if request.user.id:
            print(request.user)
            return redirect('/')

        return render(request, 'login.html')

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=id, password=password)

        if user is not None:
            login(request, user)
            context['success'] = True
            context['message'] = '로그인 되었습니다.'
        else:
            context['success'] = False
            context['message'] = '일치하는 회원정보가 없습니다.'
        
        return JsonResponse(context, content_type='application/json')



class RegisterView(View):
    '''
    회원가입 기능
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        if request.user.id:
           return redirect('/')

        return render(request, 'register.html')

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        id = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        name = request.POST['register-name']
        email = request.POST['register-email']
        phone = request.POST['register-phone']

        if password != confirm_password:
            context['success'] = False
            context['message'] = '비밀번호가 일치하지 않습니다.'
            return JsonResponse(context, content_type='application/json')

        try:
            user = User.objects.get(username=id)
            context['success'] = False
            context['message'] = '이미 존재하는 아이디입니다'
            return JsonResponse(context, content_type='application/json')
        except:
            print('사용 가능한 아이디')

        try:
            mem = Member.objects.get(mem_phone=phone)
            context['success'] = False
            context['message'] = '이미 가입한 번호입니다.'
            return JsonResponse(context, content_type='application/json')
        except:
            print('사용 가능한 번호')

        try:
            user = User.objects.get(email=email)
            context['success'] = False
            context['message'] = '이미 가입한 이메일입니다.'
            return JsonResponse(context, content_type='application/json')
        except:
            print('사용 가능한 이메일 주소')
            user = User.objects.create_user(
                id,
                email,
                password,
            )
            user.is_active = True
            user.save()

            userid = user.id
            mem = Member.objects.create(
                    user = User.objects.filter(id=userid).first(),
                    mem_name = name,
                    mem_phone = phone,
                    mem_point = 2000,
                    mem_level = Membership.objects.filter(level='Basic').first(),
                )
            

        context['success'] = True
        context['message'] = '회원 가입 완료'
        context['id'] = id
        context['password'] = password
        context['email'] = email
        return JsonResponse(context, content_type='application/json')


class CheckSameId(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        request.POST = json.loads(request.body)
        context = {}

        id = request.POST['username']

        try:
            user = User.objects.get(username=id)
            context['success'] = False
            return JsonResponse(context, content_type='application/json')

        except:
            context['success'] = True
        return JsonResponse(context, content_type='application/json')


class CheckSameEmail(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        request.POST = json.loads(request.body)
        context = {}

        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            context['success'] = False
            return JsonResponse(context, content_type='application/json')

        except:
            context['success'] = True
        return JsonResponse(context, content_type='application/json')

class confirmInfo(LoginRequiredMixin, View):
    '''
    회원정보 수정 전 비밀번호 확인
    '''
    template_name = 'user-account_confirm.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        user_id = request.user.id
       
        context={}
        context['member'] = Member.objects.get(user__id=user_id)
    
        return render(request, self.template_name,  context)

class ChangeMemView(View):
    '''
    회원정보 수정 기능
    '''
    template_name = 'user-account_edit.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        user_id = request.user.id
       
        context={}
        context['member'] = Member.objects.get(user__id=user_id)
    
        return render(request, self.template_name,  context)


    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
       
        password = request.POST['password']
        new_password = request.POST['new-password']
        confirm_password = request.POST['confirm-password']
        name = request.POST['new-name']
        email = request.POST['new-email']
        phone = request.POST['new-phone']

        if new_password != confirm_password:
            context['success'] = False
            context['message'] = '비밀번호가 일치하지 않습니다.'
            return JsonResponse(context, content_type='application/json')
        
        if not check_password(password, request.user.password):
            context['success'] = False
            context['message'] = '비밀번호가 틀립니다.'
            return JsonResponse(context, content_type='application/json')

        user_id = request.user.id
        #change password
        if new_password !="":
            print("new_password is not none")
            print(new_password)
            request.user.set_password(new_password)
            request.user.save()

        #change email
        user = User.objects.filter(id=user_id).update(
            email = email,
        )

        #change mem_name, mem_phone
        mem = Member.objects.filter(user__id=user_id).update(
            mem_name = name,
            mem_phone = phone,
        )

        
        context['success'] = True
        context['message'] = '회원정보가 수정되었습니다.'
        return JsonResponse(context, content_type='application/json')

def best():
    orders = pd.read_csv('orders.csv')
    df_series = orders["product_id"].value_counts()
    best = df_series.to_frame(name='Best').head(10).index.tolist()
   
    return best