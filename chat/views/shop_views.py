from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from config.models import Shop, ShopCategory, Member, CartProduct

class ShopView(View):
    template_name='shops.html'

    def get(self, request: HttpRequest):
        context = {}

        if request.user.is_authenticated:
            context['memname'] = list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
            context['cart'] = CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        context['ShopCategories'] = ShopCategory.objects.filter(deleteflag='0')
        context['ShopList'] = Shop.objects.filter(deleteflag='0')

        return render(request, self.template_name, context)
