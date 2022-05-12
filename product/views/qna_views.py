import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from datetime import datetime

from config.models import ProQna, Product, Member

class QnaPostView(View):
    '''
    상품 문의 등록
    '''

    def post(self, request: HttpRequest, *args, **kwargs):
        context={}
        request.POST = json.loads(request.body)

        title = request.POST.get('title')
        content = request.POST.get('content')
        product_id = request.POST.get('product_id')

        ProQna.objects.create(
            deleteflag='0',
            title=title,
            content=content,
            member=Member.objects.get(user=request.user),
            product=Product.objects.get(id=product_id),
            answer_flag='0',
        )
        
        context['success']=True

        return JsonResponse(context, content_type='application/json')

class QnaTableView(View):
    '''
    상품 상세 페이지의 상품 문의

    DataTable에 넣을 문의 목록을 받아옵니다.
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['qna']=list(ProQna.objects.filter(deleteflag='0').order_by('-created_at')\
                                        .values('created_at', 'answer_flag', 'title', 'id', 'member__mem_name', 'password'))

        return JsonResponse(context, content_type='application/json')
