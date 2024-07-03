from django.urls import path
from .views import BillingAddressListAPIView, BillingAddressDetailAPIView

urlpatterns = [
    path('', BillingAddressListAPIView.as_view(), name='billing-address-list'),
    path('<int:pk>/', BillingAddressDetailAPIView.as_view(), name='billing-address-detail'),
]
