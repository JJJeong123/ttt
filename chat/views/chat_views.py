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
        
        return render(request, self.template_name, context=context)

class ProductListView(View):

    def get(self, request: HttpRequest):
        context={}
        shopId = request.GET.get('shopId')
        context['products'] = list(Product.objects.filter(shop__id=shopId, status = '1').values('name', 'price', 'description'))

        print(context['products'])

        return JsonResponse(context, content_type='application/json')

