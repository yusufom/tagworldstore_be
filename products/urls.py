from django.urls import path
from .views import ProductListView, ProductSingleView, UpdateWishListApiView, GetProductReviewtView, ProductReviewtView, GetAllWishListApiView, CreateWishListApiView, ClearWishListApiView
from core.views import SlideView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('<str:slug>/', ProductSingleView.as_view()),
    path('wishlist/update/', UpdateWishListApiView.as_view()),
    path('wishlist/create/', CreateWishListApiView.as_view()),
    path('wishlist/clear/', ClearWishListApiView.as_view()),
    path('wishlist/list/', GetAllWishListApiView.as_view()),
    path('review/<int:id>/', GetProductReviewtView.as_view()),
    path('review/create/', ProductReviewtView.as_view()),
    path('slides/views/', SlideView.as_view()),
]