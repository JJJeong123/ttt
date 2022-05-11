from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateView
from typing import Any, Dict
import json
from django.db.models import F
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.contrib.auth.mixins import LoginRequiredMixin

from config.models import Comment, Member, Order, OrderProduct, Product

class ReviewView(LoginRequiredMixin, View):
    '''
    후기

    작성 완료 후기/ 미작성 후기
    '''
    template_name = 'review.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        images=[]
        images_ordered=[]

        reviews_id=list(Comment.objects.filter(deleteflag='0', member__user=request.user).values('id').order_by('-created_at'))
        ordered_products = list(OrderProduct.objects.filter(order__member__user=request.user, status='4', deleteflag='0', review_flag='0')\
                      .values('id', 'order__created_at', 'product__id', 'product__name', 'amount'))

        for id in reviews_id:
            images.append(Comment.objects.get(id=id.get('id')))

        for id in ordered_products:
            images_ordered.append(Product.objects.get(id=id.get('product__id')))

        # 작성 완료 후기
        context['reviews']=list(Comment.objects.filter(deleteflag='0', member__user=request.user)\
                                    .values('content', 'orderproduct__product__name', 'orderproduct__product__id','created_at')\
                                      .order_by('-created_at')\
                                      .annotate(rate=Cast(F('rate') * 20, IntegerField())))
        context['images']=images

        # 미작성 후기
        context['ordered_products']=ordered_products
        context['images_ordered']=images_ordered

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context={}

        orderproduct_id = request.POST.get('review-id')
        rate = request.POST.get('review-rate')
        content = request.POST.get('review-content')
        img = request.FILES.get('review-img')
        print(img)
        if OrderProduct.objects.filter(id=orderproduct_id).values_list('review_flag')=='1':
            context['success']=False
        
        Comment.objects.create(
            rate=rate,
            content=content,
            member=Member.objects.get(user=request.user),
            reply_flag='0',
            comment_img=img,
            deleteflag='0',
            orderproduct=OrderProduct.objects.get(id=orderproduct_id)
        )

        OrderProduct.objects.filter(id=orderproduct_id).update(
            review_flag='1'
        )
        
        context['success']=True

        return JsonResponse(context, content_type='application/json')

class ReviewPostView(LoginRequiredMixin, TemplateView):
    '''
    후기 등록
    '''
    template_name = 'review_post.html' 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context={}

        orderproduct_id = list(OrderProduct.objects.filter(id=kwargs.get('id')).values_list('id', flat=True))[0]
        context['orderproduct_id'] = orderproduct_id

        return context
