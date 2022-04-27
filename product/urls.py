from django.urls import path
from . import views
from .views import product_views

app_name = 'product'

urlpatterns=[
    # path('test', test.TestView.as_view(test)),
    path('product-detail/<str:id>', product_views.ProductDetailView.as_view(), name='product-detail'),
    
]