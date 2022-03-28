from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from config.views import index, LoginView, RegisterView, CheckSameId, CheckSameEmail
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.as_view()),

    path('login', LoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(next_page='./'), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('check-same-id', CheckSameId.as_view(), name='check-same-id'),
    path('check-same-email', CheckSameEmail.as_view(), name='check-same-email'),

    #path('product/', include('product.urls')),
]
