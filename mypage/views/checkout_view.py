import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db.models import IntegerField
from django.db.models.functions import Cast

from config.models import Product, Order, OrderProduct
from product.views.product_views import doesCartExist


class CheckoutView(LoginRequiredMixin, View):
    '''
    결제창
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        return render(request, 'checkout.html', context)

class OrderHistoryView(LoginRequiredMixin, View):
    '''
    주문내역
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        orders=[]
        products=[]
        num=[] # 주문 당 상품 개수
        amount=[] # 주문의 첫 번째 상품 개수
        first_item=[] # 주문의 첫 번째 상품 정보

        # user's orders
        orders=list(Order.objects.filter(deleteflag='0', member__user_id=request.user.id).order_by('-created_at').values('id', 'order_no', 'status', 'created_at', 'total_price'))

        # products of each 
        for order in orders:
            product=list(OrderProduct.objects.filter(deleteflag='0', order=order['id']).values('product__id', 'product__price', 'amount', 'product__name'))
            products.append(product)
            first_item.append(Product.objects.get(id=product[0]['product__id']))
            num.append(product[0]['amount'])

        for product in products:
            amount.append(len(product)-1)

        context={
            'first_item': first_item,
            'amount': amount,
            'orders': orders,
            'num': num,
        }
        return render(request, 'order_history.html', context)

class OrderDetailView(LoginRequiredMixin, View):
    '''
    주문내역 상세
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        main_imgs=[]

        id = kwargs.get('id')

        order=Order.objects.get(id=id)
        products=list(OrderProduct.objects.filter(order=id).values('product__id', 'product__name', 'amount').annotate(total=Cast(F('amount') * F('product__price'), IntegerField())))

        for p in products:
            print(p['product__id'])
            main_imgs.append(Product.objects.get(id=p['product__id']))

        context={
            'order': order,
            'products': products,
            'items': main_imgs,
        }

        return render(request, 'order_detail.html',  context)
    
