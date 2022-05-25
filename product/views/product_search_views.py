import json
from django.http import HttpRequest, JsonResponse , HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from datetime import datetime

from config.models import Product, LikedProduct, Member, CartProduct

class ProductsView(TemplateView):
    template_name="product-search.html"

class ProductSearchView(View):
    '''
    상품 검색 페이지

    검색 결과를 출력합니다.
    '''
    def post(self, request: HttpRequest, *args, **kwargs):
        context={}
        context['memname'] = list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart'] = CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        like=[]
        keyword = request.POST.get('keyword', False)

        products = (Product.objects.filter(name__contains=keyword, deleteflag='0'))

        if request.user.is_authenticated:
            for product in list(products):
                like.append(LikedProduct.objects.filter(liked__member__user=request.user, deleteflag='0', product__id=product.id).count())
        else:
            like=""

        context['products']=products
        context['like']=like

        return render(request, 'product-search.html',  context)