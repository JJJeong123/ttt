from django.urls import path
from . import views
from .views import product_views, qna_views,product_best_views

app_name = 'product'

urlpatterns=[
    # path('test', test.TestView.as_view(test)),
    path('qna-post', qna_views.QnaPostView.as_view(), name='qna-post'),
    path('qna-table', qna_views.QnaTableView.as_view(), name='qna-table'),

    path('product-detail/<str:id>', product_views.ProductDetailView.as_view(), name='product-detail'),
    path('product-best', product_best_views.ProductBestView.as_view(), name='product-best'),
    path('product-list/<int:category>', product_views.ProductListView.as_view(), name='product-list'),
    path('product-grid', product_views.ProductGridView.as_view(), name='product-grid'),

]