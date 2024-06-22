from django.urls import path
from .views import ProductListView, ProductSingleView, WishListApiView, GetProductReviewtView, ProductReviewtView, GetAllWishListApiView
from core.views import SlideView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('<str:slug>/', ProductSingleView.as_view()),
    path('wishlist/', WishListApiView.as_view()),
    path('wishlist/list/', GetAllWishListApiView.as_view()),
    path('review/<int:id>/', GetProductReviewtView.as_view()),
    path('review/create/', ProductReviewtView.as_view()),
    path('slides/views/', SlideView.as_view()),
]