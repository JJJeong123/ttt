from django.urls import path

from .views import checkout_view, review_views, cart_views, like_views, qna_views

app_name = 'mypage'

urlpatterns=[
    path('review', review_views.ReviewView.as_view(), name='review'),
    path('review-table', review_views.ReviewTableView.as_view(), name='review-table'),
    path('review-post/<str:id>', review_views.ReviewPostView.as_view(), name='review-post'),
    path('review-detail/<str:id>', review_views.ReviewDetailView.as_view(), name='review-detail'),

    # 마이페이지
    path('cart', cart_views.CartView.as_view(), name='cart'),
    path('checkout', checkout_view.CheckoutView.as_view(), name='checkout'),
    path('order-history', checkout_view.OrderHistoryView.as_view(), name='order-history'),
    path('order-detail/<str:id>', checkout_view.OrderDetailView.as_view(), name='order-detail'),
    path('like', like_views.LikeView.as_view(), name='like'),

    path('qna', qna_views.QnaView.as_view(), name='qna'),
    path('qna-list', qna_views.QnaListView.as_view(), name='qna-list'),
    path('qna-table', qna_views.QnaTableView.as_view(), name='qna-table'),
    path('qna-detail/<str:id>', qna_views.QnaDetailView.as_view(), name='qna-detail'),

]