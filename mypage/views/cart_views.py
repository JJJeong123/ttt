import json
from django.forms import FloatField, IntegerField
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db.models import IntegerField
from django.db.models.functions import Cast

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

        if(doesCartExist is False):
            return render(request, 'cart.html',  context)

        cart=list(Cart.objects.filter(member__user_id=request.user.id).values_list('id', flat=True))[0]

        products_in_cart=list(CartProduct.objects.filter(cart=cart, deleteflag='0').values_list('product', flat=True))

        for p in products_in_cart:
            products.extend(CartProduct.objects.filter(product=p, cart=cart).values('product__main_img', 'product__name', 'product__price', 'amount', 'product__id').annotate(total=Cast(F('amount') * F('product__price'), IntegerField())))
            main_imgs.append(Product.objects.get(id=p))

        #context['products']=zip(products, main_imgs)
        context['main_imgs']=main_imgs
        context['products']=products

        print(main_imgs)

        return render(request, 'cart.html',  context)
    
