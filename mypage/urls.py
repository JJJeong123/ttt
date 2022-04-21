from django.urls import path
from .views import review_views

app_name = 'mypage'

urlpatterns=[
    path('review', review_views.ReviewView.as_view(), name='review'),
    path('review-table', review_views.ReviewTableView.as_view(), name='review-table'),
    path('review-post/<str:id>', review_views.ReviewPostView.as_view(), name='review-post'),
    path('review-detail/<str:id>', review_views.ReviewDetailView.as_view(), name='review-detail'),
]