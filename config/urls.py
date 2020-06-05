"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from acceptances.views import AcceptanceViewSet, ItemViewSet
from accounting.views import ProfossViewSet
from accounts.views import UserViewSet
from carts.views import CartViewSet
from products.views import ProductViewSet
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('admin/', admin.site.urls),
]


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', UserViewSet, basename='user')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'acceptances', AcceptanceViewSet, basename='acceptance')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'profoss', ProfossViewSet, basename='profoss')
urlpatterns += router.urls
