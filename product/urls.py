from django.urls import path
from . import views
from .views import product_views, qna_views,product_best_views

app_name = 'product'

urlpatterns=[
    # path('test', test.TestView.as_view(test)),
    path('product-detail/<str:id>', product_views.ProductDetailView.as_view(), name='product-detail'),
    path('qna-post', qna_views.QnaPostView.as_view(), name='qna-post'),
    path('product-best', product_best_views.ProductBestView.as_view(), name='product-best')    
]