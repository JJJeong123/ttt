import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from config.models import Qna, QnaCategory, Member, Order

class QnaView(LoginRequiredMixin, View):
    '''
    1:1문의
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['cats']=list(QnaCategory.objects.filter(deleteflag='0').values_list('name', flat=True))
        context['orders']=list(Order.objects.filter(deleteflag='0', member__user=request.user).values_list('order_no', flat=True))
        
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

        return JsonResponse(context, content_type='application/json')

