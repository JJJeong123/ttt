import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from config.models import ProQna, ProQnaAnswer

class ProductQnaListView(View):
    '''
    1:1 문의 목록
    '''
    template_name = 'product_qna_list.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class ProductQnaTableView(View):
    '''
    1:1 문의 목록

    DataTable에 넣을 문의 목록을 받아옵니다.
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['qna']=list(ProQna.objects.filter(deleteflag='0', member__user=request.user)\
                                        .values('created_at', 'answer_flag', 'title', 'id', 'product__name'))

        return JsonResponse(context, content_type='application/json')


class ProductQnaDetailView(LoginRequiredMixin, View):
    '''
    상품 문의 상세 페이지
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        id = kwargs.get('id')
        context={}

        context['qna'] = list(ProQna.objects.filter(id=id).values('title', 'content', 'created_at', 'answer_flag'))[0]

        # 문의 답변이 등록되어 있다면 
        if context['qna'].get('answer_flag')=='1':
            context['answer']=ProQnaAnswer.objects.get(qna__id=id)
        
        return render(request, 'product_qna_detail.html', context)