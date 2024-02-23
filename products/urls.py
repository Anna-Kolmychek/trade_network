from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet
from products.apps import ProductsConfig

app_name = ProductsConfig.name

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls))
]
