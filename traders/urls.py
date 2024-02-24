from django.urls import path, include
from rest_framework.routers import DefaultRouter

from traders.views import TraderViewSet
from traders.apps import TradersConfig

app_name = TradersConfig.name

router = DefaultRouter()

router.register(r'', TraderViewSet, basename='trader')

urlpatterns = [
    path('', include(router.urls))
]
