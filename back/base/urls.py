from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView, ProductViewSet, CartView, CartItemView,
    CheckoutView, OrderListView, OrderDetailView, ReviewViewSet,
    WishlistView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

app_name = 'base'

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # Products (via router)
    path('', include(router.urls)),
    
    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/<uuid:item_id>/', CartItemView.as_view(), name='cart-item'),
    
    # Checkout & Orders
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),
    
    # Reviews
    path('products/<uuid:product_id>/reviews/', 
         ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='product-reviews'),
    
    # Wishlist
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/<uuid:product_id>/', WishlistView.as_view(), name='wishlist-item'),
]