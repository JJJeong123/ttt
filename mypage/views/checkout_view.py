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


class CheckoutView(LoginRequiredMixin, View):
    '''
    결제창
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        return render(request, 'checkout.html',  context)
    
