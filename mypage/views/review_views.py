from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateView
from typing import Any, Dict
import json
#from django.contrib.auth.mixins import LoginRequiredMixin

from config.models import Comment, Member, OrderProduct, Product

class ReviewView(View):
    template_name = 'review_list.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class ReviewTableView(View):
    '''
    리뷰 작성 가능한 상품 / 작성한 리뷰

    Datatable에 넣을 데이터를 받아옵니다.
    '''
    def get(self, request: HttpRequest):
        user_id=request.user.id

        ReviewProduct = list(OrderProduct.objects.filter(order__member__user_id=user_id, status='4', deleteflag='0').values('id', 'order__date','product__shop__shop_name', 'product__name'))
        Review = list(Comment.objects.filter(member__user_id=user_id, deleteflag='0').values('id', 'created_at', 'product__shop__shop_name', 'product__name', 'rate'))

        context = {
            'reviewProduct': ReviewProduct,
            'review': Review,
        }

        return JsonResponse(context, content_type='application/json')


class ReviewPostView(TemplateView):
    '''
    리뷰 등록
    '''
    template_name = 'review_post.html' 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context={}

        reviewPro = list(OrderProduct.objects.filter(id=kwargs.get('id')).values('product__id', 'order__date','product__shop__shop_name', 'product__name'))
        context['reviewPro'] = reviewPro[0]

        return context

    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
   
        mainImg = request.FILES.getlist('mainImg')
        Rate = request.POST.get('rate')
        Content = request.POST.get('content')
        proId = request.POST.get('proId')

        for image in mainImg:
            Comment.objects.create(
                member = Member.objects.get(user=request.user),
                product = Product.objects.get(id=proId),
                comment_img = image,
                content = Content,
                rate = Rate,
                reply_flag = '0',
                deleteflag='0'
            )

        context['success']=True
        return JsonResponse(context, content_type='application/json')


class ReviewDetailView(View):
    '''
    리뷰 상세 페이지
    '''
    template_name = 'review_detail.html' 

    def get(self, request: HttpRequest, *args, **kwargs):
        id = kwargs.get('id')
        comment = Comment.objects.get(id=id)
        context={}
        context['comment'] = comment
        return render(request, self.template_name,  context)