from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from config.models import Shop

class ChatView(View):
    template_name='chat.html'

    def get(self, request: HttpRequest):
        context={}
        shopId = request.GET.get('shopId')
        shop = Shop.objects.get(id=shopId)
      
        context['shop'] = shop
        
        return render(request, self.template_name, context=context)
