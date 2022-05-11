import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from datetime import datetime

import pandas as pd
import numpy as np
import mlxtend
from mlxtend.frequent_patterns import fpgrowth, association_rules, apriori
from mlxtend.preprocessing import TransactionEncoder
import openpyxl

from config.models import Product, CartProduct, Cart, Member, Liked, LikedProduct, OrderProduct

class ProductBestView(View):
    '''
    상품 상세 페이지
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        id = kwargs.get('id')
        #product = Product.objects.get(id=id)
        product = recommend(410)
        product = Product.objects.get(id=1)
        print(product)
        context['product'] = product
        print(product)
        return render(request, 'product-best.html',  context)

def recommend(product_id):
    productid = list(Product.objects.filter(id=product_id).values_list('id',flat=True))[0]
    orders = pd.read_csv('orders.csv')
    grouped_df = orders.groupby('order_id').agg({"product_id": lambda x: list(set(x))})
    dataset = list(grouped_df["product_id"])
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = fpgrowth(df, min_support=0.8, use_colnames=True)
    res = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    res1 = res[['antecedents', 'consequents', 'support', 'confidence','lift']]
    rules = res1[res['confidence'] >= 1]
    print(rules)
    
   
    
    for i,row in rules.iterrows():
        for x in row['antecedents']:
            if x==productid:
                rec_id= list(row['consequents'])[0]
                
        
                
               

        
       
        

      
        

    
    
    
    
    """
 
    grouped_df = orders.groupby('order_id').agg({"product_id": lambda x: list(set(x))})
    #dataset = list(grouped_df["name"])
    #print(dataset)
    dataset = list(grouped_df["product_id"])
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True) #fpgrowth 바꾸기
    print(frequent_itemsets)
    res = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    #print(res)
    """
    """
   
    #orders = pd.DataFrame(list(OrderProduct.objects.all().values('order_id','product_id')))
    #products =  pd.DataFrame(list(Product.objects.all().values('id','name')))
    #products.rename(columns={'id':'product_id'},inplace = True)
    #data = pd.merge(orders,products,on='product_id',how="inner")
    #df = data[["order_id", "name"]]
    #products.to_excel("products.xlsx",index=False)
    #orders.to_excel("orders.xlsx",index=False)
    grouped_df = orders.groupby('order_id').agg({"product_id": lambda x: list(set(x))})
    #dataset = list(grouped_df["name"])
    #print(dataset)
    dataset = list(grouped_df["product_id"])
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True) #fpgrowth 바꾸기
    #print(frequent_itemsets)
    res = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    #print(res)
    res1 = res[['antecedents', 'consequents', 'support', 'confidence','lift']]
    rules = res1[res['confidence'] >= 1]
    #print(list(rules['antecedents']))
    #if frozenset({id}) in list(rules['antecedents']):
    #    print(rules["consequents"])
    print(rules)
    #rules = rules[rules['antecedents']==frozenset({id})]
    #print(rules)
    
    
     for result_id in list(rules['consequents'])[0]:
        product = Product.objects.get(id=result_id)
    return product 
    """
    #print(frozenset({id}).difference(rules['antecedents']))
   
    #rules["consequents"] = rules["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    
   
   
    



  
    