from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from config.models import Shop, Product

class ChatView(View):
    template_name='chat.html'

    def get(self, request: HttpRequest):
        context={}
        shopId = request.GET.get('shopId')
        shop = Shop.objects.get(id=shopId)
      
        context['shop'] = shop
        context['products'] = (Product.objects.filter(shop__id=shopId, status = '1', deleteflag='0'))

        
        return render(request, self.template_name, context=context)

class ProductListView(View):

    def get(self, request: HttpRequest):
        context={}

        shopId = request.GET.get('shopId')
        context['products'] = (Product.objects.filter(shop__id=shopId, status = '1', deleteflag='0'))

        return JsonResponse(context, content_type='application/json')

