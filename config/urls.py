from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from config import settings
from config.views import index, LoginView, RegisterView, CheckSameId, CheckSameEmail
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.as_view(), name='index'),

    path('login', LoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(next_page='./'), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('check-same-id', CheckSameId.as_view(), name='check-same-id'),
    path('check-same-email', CheckSameEmail.as_view(), name='check-same-email'),

    path('chat/', include('chat.urls')),
    path('mypage/', include('mypage.urls')),
    path('product/', include('product.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
