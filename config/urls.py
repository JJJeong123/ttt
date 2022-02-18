from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from config.views import index
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.as_view()),

    # path('product/', include('product.urls')),
]
