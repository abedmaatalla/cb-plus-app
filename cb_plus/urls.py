"""cb_plus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from main import views
from drf_yasg import openapi

import views

schema_view = get_schema_view(
   openapi.Info(
      title="CB+ API",
      default_version='v1',
   ),
   public=False,
   permission_classes=(permissions.AllowAny,),
)

public_router = routers.DefaultRouter()
public_router.register(r'stock_expiration', views.StockExpirationViewSet, base_name='stock_expiration')
public_router.register(r'stock_readings', views.StockViewSet, base_name='stock_readings')
public_router.register(r'products', views.ProductViewSet, base_name='products')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/public/', include(public_router.urls)),

    path('', views.StockReadingListView.as_view(), name='stock_reading_list'),

    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),

    path('stocks/', views.StockListView.as_view(), name='stock_list'),
    path('stocks/add/', views.StockCreateView.as_view(), name='stock_add'),
    path('stocks/<int:pk>/edit/', views.StockUpdateView.as_view(), name='stock_edit'),
]
