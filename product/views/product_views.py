import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from datetime import datetime

from config.models import Product, CartProduct, Cart, Member


class ProductDetailView(View):
    '''
    상품 상세 페이지
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        id = kwargs.get('id')
        product = Product.objects.get(id=id)

        context['product'] = product

        return render(request, 'product-detail.html',  context)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context={}
        request.POST = json.loads(request.body)

        id = kwargs.get('id')
        amount = request.POST.get('amount')

        # Create a cart if cart does not exist
        if(doesCartExist(request.user.id) is False):
            Cart.objects.create(
                member=Member.objects.filter(user_id=request.user.id).first(),
                deleteflag='0',
            )
        
        # Add product to cart
        cart_id=list(Cart.objects.filter(member__user_id=request.user.id).values_list('id', flat=True))[0]
        
        if(isAlreadyInCart(cart_id, id)):
            CartProduct.objects.filter(cart=cart_id).update(
                amount = F('amount')+amount,
                updated_at = datetime.now(),
            )
        else:
            CartProduct.objects.create(
                amount=amount,
                cart=Cart.objects.filter(member__user_id=request.user.id).first(),
                product=Product.objects.filter(id=id).first(),
                deleteflag='0',
            )

        context['success']=True

        return JsonResponse(context, content_type='application/json')

def doesCartExist(id):
    if (Cart.objects.filter(member__user_id=id).count() > 0):
        return True
    return False

def isAlreadyInCart(cart_id, product_id):
    if(CartProduct.objects.filter(cart=cart_id, product=product_id).count() > 0):
        return True
    return False