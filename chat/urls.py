from django.urls import path

from . import views
from .views import shop_views

app_name = 'chat'

urlpatterns=[

    #판매 관리
    path('shop-list', shop_views.ShopView.as_view(), name='shop-list'),

]