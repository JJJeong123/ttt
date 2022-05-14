import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from datetime import datetime

from config.models import ProQna, Product, Member, ProQnaAnswer

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
        password = request.POST.get('password')

        ProQna.objects.create(
            deleteflag='0',
            title=title,
            content=content,
            member=Member.objects.get(user=request.user),
            product=Product.objects.get(id=product_id),
            password=password,
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
        answer=[]
        qnas=[]
        #qna=list(ProQna.objects.filter(deleteflag='0')\
        #                        .values('created_at', 'answer_flag', 'title', 'id', 'member__mem_name', 'password', 'content'))

        qna=list(ProQna.objects.filter(deleteflag='0')\
                                .values('created_at', 'answer_flag', 'title', 'id', 'member__mem_name', 'password', 'content'))

        for i in range(0, len(qna)):
            try: 
                if ProQnaAnswer.objects.filter(qna__id=qna[i].get('id')).count() <= 0:
                    qna[i]['answer_content']=None
                    #answer.append({'answer_content': None})
                else:
                    qna[i]['answer_content']=list(ProQnaAnswer.objects.filter(qna__id=qna[i].get('id')).values_list('content', flat=True))[0]

            except ProQnaAnswer.DoesNotExist:
                answer.append({'answer_content': None})

        context={
          'qna': qna,
        }
        return JsonResponse(context, content_type='application/json')
