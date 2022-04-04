from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from config.models import Shop, ShopCategory

class ShopView(View):
    template_name='shops.html'

    def get(self, request: HttpRequest):
        context = {}

        context['ShopCategories'] = ShopCategory.objects.filter(deleteflag='0')
        context['ShopList'] = Shop.objects.filter(deleteflag='0')

        return render(request, self.template_name, context)
