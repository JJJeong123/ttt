import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from datetime import datetime
from tkinter import N

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import fpgrowth, association_rules, apriori
from mlxtend.preprocessing import TransactionEncoder

from config.models import Product, CartProduct, Cart, Member, Liked, LikedProduct, OrderProduct


class ProductDetailView(View):
    '''
    상품 상세 페이지
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        if request.user.is_authenticated:
            context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
            context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()


        id = kwargs.get('id')
        product = Product.objects.get(id=id)

        recbox = recommend(id)
        queryset = Product.objects.filter(id__in=recbox)
        
        if len(list(queryset))> 5:
            queryset=queryset[:5]
        else:
            context['range'] = range(5-len(queryset))

        context['related_products'] = queryset
        context['product'] = product
        context['Liked'] = isAlreadyInList(request.user.id, id)

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
            CartProduct.objects.filter(cart=cart_id, product=id).update(
                amount = F('amount')+amount,
                updated_at = datetime.now(),
                deleteflag='0',
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

class ProductListView(View):
    '''
    카테고리별 상품 리스트
    '''
    template_name = 'product-list.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        if request.user.is_authenticated:
            context['memname']=list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
            context['cart']=CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        return render(request, self.template_name, context)#

class ProductGridView(View):
    '''
    카테고리별 상품 리스트
    '''

    def get(self, request: HttpRequest):
        context={}

        imgs=[]
        like=[]

        category=request.GET.get('cat')
        products=list(Product.objects.filter(deleteflag='0', pro_subcategory=category)
                                            .values('id', 'name', 'price'))
        
        for product in products:
            imgs.append("https://jjjtttbucket.s3.ap-northeast-2.amazonaws.com/media/"+list(Product.objects.filter(id=product.get('id')).values_list('main_img', flat=True))[0])

        if request.user.is_authenticated:
            for product in products:
                like.append(LikedProduct.objects.filter(liked__member__user=request.user, deleteflag='0', product__id=product.get('id')).count())
                context['like']=like
        else:
            context['like']=""
        
        context['products']=products
        context['imgs']=imgs
        context['success']=True

        return JsonResponse(context, content_type='application/json')

def recommend(product_id):
    productid = list(Product.objects.filter(id=product_id).values_list('id',flat=True))[0]
    orders = pd.read_csv('orders.csv')
    grouped_df = orders.groupby('order_id').agg({"product_id": lambda x: list(set(x))})
    dataset = list(grouped_df["product_id"])

    df_series = orders["product_id"].value_counts()
    best = df_series.to_frame(name='Best').head(10).index.tolist()
    queryset = Product.objects.filter(id__in=best)
   
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = fpgrowth(df, min_support=0.75, use_colnames=True)
    res = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    res1 = res[['antecedents', 'consequents', 'support', 'confidence','lift']]
    rules = res1[res['confidence'] >= 1].reset_index(drop = True)
    recommend_dict = {}
    
    for i in range(len(rules)) :
        key = list(rules.iloc[i,0])
        values = list(rules.iloc[i,1])
        if len(key) == 1 :
            try : 
                recommend_dict[key[0]] += values
            except :
                recommend_dict[key[0]] = values
        recommend_dict[key[0]] = list(set(recommend_dict[key[0]]))
    
    val = []
    
    for key in recommend_dict.keys():
        if key==productid :
            val = recommend_dict[productid]
            break
    return val
    
def doesCartExist(id):
    if (Cart.objects.filter(member__user_id=id).count() > 0):
        return True
    return False

def isAlreadyInCart(cart_id, product_id):
    if(CartProduct.objects.filter(cart=cart_id, product=product_id).count() > 0):
        return True
    return False

def isAlreadyInList(user_id, product_id):
    if(LikedProduct.objects.filter(liked__member__user_id=user_id, product=product_id, deleteflag='0').count()>0):
        return True
    return False