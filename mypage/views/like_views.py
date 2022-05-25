import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Cast
from datetime import datetime
from config.models import Product, Liked, LikedProduct, Member, CartProduct


class LikeView(LoginRequiredMixin, View):
    '''
    찜한상품
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        user_id=request.user.id
        liked_products=[]

        if(doesListExist(user_id) is False):
            return render(request, 'like.html', context)
        
        products=list(LikedProduct.objects.filter(liked__member__user_id=user_id, deleteflag='0').order_by('-updated_at').values_list('product__id', flat=True))
        for product in products:
            liked_products.append(Product.objects.get(id=product))
        
        context={
          'liked_products': liked_products,
          'memname': list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0],
          'cart': CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count(),
          'memname': list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0],
          'cart': CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()
        }

        return render(request, 'like.html', context)
    
    def put(self, request: HttpRequest, *args, **kwargs):
        context={}
        request.PUT = json.loads(request.body)

        id = request.PUT.get('id')
        isLiked = request.PUT.get('isLiked')
        user_id=request.user.id

        # Create a Liked if cart does not exist
        if(doesListExist(user_id) is False):
            Liked.objects.create(
                member=Member.objects.filter(user_id=user_id).first(),
                deleteflag='0',
            )

        # Add product to wish list
        list_id=list(Liked.objects.filter(member__user_id=user_id).values_list('id', flat=True))[0]
        
        # LikedProduct에 존재하지 않는다면
        if(existsInList(list_id, id) is False):
            LikedProduct.objects.create(
                product=Product.objects.filter(id=id).first(),
                liked=Liked.objects.filter(id=list_id).first(),
                deleteflag='0',
            )
        else:
            liked_product_id=list(LikedProduct.objects.filter(liked_id__member_id__user_id=user_id, product_id=id).values_list('id', flat=True))[0]

            # LikedProduct에 존재 & 찜한 상태
            if(isLiked is True):
                LikedProduct.objects.filter(id=(liked_product_id)).update(
                    deleteflag='1',
                    updated_at=datetime.now(),
                )
            # LikedProduct에 존재 & 찜x
            else:
                LikedProduct.objects.filter(id=(liked_product_id)).update(
                    deleteflag='0',
                    updated_at=datetime.now(),
                )

        context['success']=True

        return JsonResponse(context, content_type='application/json')
    
    def delete(self, request:HttpRequest, *args, **kwargs):
        context={}
        request.PUT = json.loads(request.body)

        product_id = request.PUT.get('product_id')
        liked_id = list(Liked.objects.filter(member__user_id=request.user.id).values_list('id'))[0]

        LikedProduct.objects.filter(liked=liked_id, product=product_id).update(
            deleteflag='1',
            updated_at=datetime.now(),
        )
        context['success']=True

        return JsonResponse(context, content_type='application/json')

def doesListExist(id):
    if (Liked.objects.filter(member__user_id=id).count() > 0):
        return True
    return False

def isAlreadyInList(liked_id, product_id):
    if(LikedProduct.objects.filter(liked__id=liked_id, product=product_id, deleteflag='0').exists()):
        return True
    return False

def existsInList(liked_id, product_id):
    if(LikedProduct.objects.filter(liked__id=liked_id, product=product_id).exists()):
        return True
    return False