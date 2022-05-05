import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from config.models import Qna, QnaAnswer, QnaCategory, Member, Order

class QnaView(LoginRequiredMixin, View):
    '''
    1:1 문의 등록
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['cats']=list(QnaCategory.objects.filter(deleteflag='0').values_list('name', flat=True))
        context['orders']=list(Order.objects.filter(deleteflag='0', member__user=request.user).values_list('order_no', flat=True))
        
        return render(request, 'qna.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context={}

        cat = request.POST.get('qna-cat')
        title = request.POST.get('qna-title')
        content = request.POST.get('qna-content')
        img = request.FILES.get('qna-img')

        Qna.objects.create(
            title=title,
            content=content,
            member=Member.objects.get(user=request.user),
            category=QnaCategory.objects.get(name=cat),
            answer_flag='0',
            qna_img=img,
            deleteflag='0',
        )

        return JsonResponse(context, content_type='application/json')

class QnaListView(View):
    '''
    1:1 문의 목록
    '''
    template_name = 'qna_list.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class QnaTableView(LoginRequiredMixin, View):
    '''
    1:1 문의 목록

    DataTable에 넣을 문의 목록을 받아옵니다.
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['qna']=list(Qna.objects.filter(deleteflag='0', member__user=request.user).values('created_at', 'answer_flag', 'title', 'id'))

        return JsonResponse(context, content_type='application/json')

class QnaDetailView(LoginRequiredMixin, View):
    '''
    1:1 문의 상세 페이지
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        id = kwargs.get('id')
        context={}

        context['qna'] = list(Qna.objects.filter(id=id).values('category', 'title', 'content', 'created_at'))[0]
        context['image']=Qna.objects.get(id=id)

        # 문의 답변이 등록되어 있다면 
        if context['image'].answer_flag=='1':
            context['answer']=QnaAnswer.objects.get(qna__id=id)
        
        return render(request, 'qna_detail.html', context)