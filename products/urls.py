from django.urls import path
from .views import ProductListView, ProductSingleView


urlpatterns = [
    path('', ProductListView.as_view()),
    path('<str:slug>', ProductSingleView.as_view()),
]