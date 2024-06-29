from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet, CreateCartMultiple

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('create_multiple/', CreateCartMultiple.as_view())
    
]
