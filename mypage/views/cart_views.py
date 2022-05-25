import json
from django.forms import FloatField, IntegerField
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db.models import IntegerField
from django.db.models.functions import Cast
from datetime import datetime

from config.models import Product, CartProduct, Cart, Member
from product.views.product_views import doesCartExist


class CartView(LoginRequiredMixin, View):
    '''
    장바구니
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        products=[]
        main_imgs=[]
        total_price=0

        if(doesCartExist is False):
            return render(request, 'cart.html',  context)

        cart=list(Cart.objects.filter(member__user_id=request.user.id).values_list('id', flat=True))[0]
        products_in_cart=list(CartProduct.objects.filter(cart=cart, deleteflag='0').order_by('-updated_at').values_list('product', flat=True))

        for p in products_in_cart:
            products.extend(CartProduct.objects.filter(product=p, cart=cart, deleteflag='0').order_by('-updated_at').values('product__main_img', 'product__name', \
                'product__price', 'amount', 'product__id', 'cart__id').annotate(total=Cast(F('amount') * F('product__price'), IntegerField())))
            main_imgs.append(Product.objects.get(id=p))

        for p in products:
            total_price=total_price+p.get('total')

        #context['products']=zip(products, main_imgs)
        context['main_imgs']=main_imgs
        context['products']=products
        context['total_price']=total_price
        context['memname'] = list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart'] = CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        return render(request, 'cart.html',  context)
    
    def delete(self, request: HttpRequest, *args, **kwargs):
        context={}
        request.DELETE = json.loads(request.body)

        product_id = request.DELETE.get('product_id')
        cart_id = request.GET.get('cart_id')

        CartProduct.objects.filter(cart=cart_id, product=product_id).update(
            amount=0,
            deleteflag='1',
            deleted_at=datetime.now(),
        )
        context['success']=True

        return JsonResponse(context, content_type='application/json')

    def put(self, request: HttpRequest, *args, **kwargs):
        context={}
        request.PUT = json.loads(request.body)

        cart_id=list(Cart.objects.filter(member__user_id=request.user.id).values_list('id', flat=True))[0]
        product_id = request.PUT.get('product_id')
        amount = request.PUT.get('amount')

        CartProduct.objects.filter(cart=cart_id, product=product_id).update(
            amount=amount,
        )
        context['success']=True

        return JsonResponse(context, content_type='application/json')
