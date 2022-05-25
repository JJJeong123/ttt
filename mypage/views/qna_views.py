import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from config.models import Qna, QnaAnswer, QnaCategory, Member, Order, CartProduct

class QnaView(LoginRequiredMixin, View):
    '''
    1:1 문의 등록
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        
        context['cats']=list(QnaCategory.objects.filter(deleteflag='0').values_list('name', flat=True))
        context['orders']=list(Order.objects.filter(deleteflag='0', member__user=request.user).values_list('order_no', flat=True))
        
        context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()
        
        return render(request, 'qna_post.html', context)

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

        context['success']=True

        return JsonResponse(context, content_type='application/json')

    def delete(self, request:HttpRequest):
        context={}
        request.DELETE = json.loads(request.body)

        qna_id=request.DELETE.get('qna_id')
        
        try:
            Qna.objects.filter(id=qna_id).update(
                deleteflag='1',
                deleted_at=datetime.now(),
            )
            context['success']=True
        
        except Exception as e:
            context['success']=False

        return JsonResponse(context, content_type='application/json')

class QnaListView(View):
    '''
    1:1 문의 목록
    '''
    template_name = 'qna_list.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        return render(request, self.template_name, context)


class QnaTableView(LoginRequiredMixin, View):
    '''
    1:1 문의 목록

    DataTable에 넣을 문의 목록을 받아옵니다.
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['qna']=list(Qna.objects.filter(deleteflag='0', member__user=request.user).order_by('-created_at')\
                                      .values('created_at', 'answer_flag', 'title', 'id'))

        return JsonResponse(context, content_type='application/json')

class QnaDetailView(LoginRequiredMixin, View):
    '''
    1:1 문의 상세 페이지
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        id = kwargs.get('id')
        context={}
        context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        context['qna'] = list(Qna.objects.filter(id=id).values('category', 'title', 'content', 'created_at', 'answer_flag'))[0]
        context['image']=Qna.objects.get(id=id)

        # 문의 답변이 등록되어 있다면 
        if context['image'].answer_flag=='1':
            context['answer']=QnaAnswer.objects.get(qna__id=id)
        
        return render(request, 'qna_detail.html', context)