import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from config.models import ProQna, ProQnaAnswer, Member, CartProduct

class ProductQnaListView(LoginRequiredMixin, View):
    '''
    1:1 문의 목록
    '''
    template_name = 'product_qna_list.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()
        
        return render(request, self.template_name, context)
    
    def delete(self, request:HttpRequest):
        context={}
        request.DELETE = json.loads(request.body)

        qna_id=request.DELETE.get('qna_id')
        
        try:
            ProQna.objects.filter(id=qna_id).update(
                deleteflag='1',
                deleted_at=datetime.now(),
            )
            context['success']=True
        
        except Exception as e:
            context['success']=False

        return JsonResponse(context, content_type='application/json')


class ProductQnaTableView(LoginRequiredMixin, View):
    '''
    1:1 문의 목록

    DataTable에 넣을 문의 목록을 받아옵니다.
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['qna']=list(ProQna.objects.filter(deleteflag='0', member__user=request.user).order_by('-created_at')\
                                        .values('created_at', 'answer_flag', 'title', 'id', 'product__name'))

        return JsonResponse(context, content_type='application/json')


class ProductQnaDetailView(LoginRequiredMixin, View):
    '''
    상품 문의 상세 페이지
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        id = kwargs.get('id')
        context={}
        context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        context['qna'] = list(ProQna.objects.filter(id=id).values('title', 'content', 'created_at', 'answer_flag', 'id'))[0]

        # 문의 답변이 등록되어 있다면 
        if context['qna'].get('answer_flag')=='1':
            context['answer']=ProQnaAnswer.objects.get(qna__id=id)
        
        return render(request, 'product_qna_detail.html', context)