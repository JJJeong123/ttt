from django.urls import path

from . import views
from .views import shop_views, chat_views

app_name = 'chat'

urlpatterns=[

    #점포 리스트
    path('shop-list', shop_views.ShopView.as_view(), name='shop-list'),
    #채팅 화면
    path('chat-page', chat_views.ChatView.as_view(), name='chat-page'),
    #해당 점포의 상품 리스트
    path('product-list', chat_views.ProductListView.as_view(), name='product-list'),

]