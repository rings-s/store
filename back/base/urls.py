# base/urls.py

from django.urls import path
from .views import (
    # Categories
    CategoryListCreateView, CategoryDetailView,
    # Brands
    BrandListCreateView, BrandDetailView,
    # Products
    ProductListCreateView, ProductDetailView, ProductSearchView,
    ProductImageUploadView, ProductVariantView, StockUpdateView,
    # Cart
    CartView, AddToCartView, UpdateCartItemView, RemoveFromCartView,
    ClearCartView,
    # Orders
    OrderListCreateView, OrderDetailView, CheckoutView,
    OrderStatusUpdateView, OrderCancelView,
    # Payment
    PaymentProcessView, PaymentStatusView,
    # Delivery
    DeliveryStatusView, DeliveryUpdateView,
    # Reviews
    ReviewListCreateView, ReviewDetailView, ProductReviewsView,
    # Wishlist
    WishlistView, AddToWishlistView, RemoveFromWishlistView,
    # Coupons
    CouponListView, CouponValidateView, ApplyCouponView,
    # Analytics
    DashboardStatsView, SalesReportView
)

app_name = 'base'

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    
    # Brands
    path('brands/', BrandListCreateView.as_view(), name='brand_list_create'),
    path('brands/<uuid:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    
    # Products
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/search/', ProductSearchView.as_view(), name='product_search'),
    path('products/<uuid:pk>/images/', ProductImageUploadView.as_view(), name='product_images'),
    path('products/<uuid:pk>/variants/', ProductVariantView.as_view(), name='product_variants'),
    path('products/<uuid:pk>/stock/', StockUpdateView.as_view(), name='stock_update'),
    path('products/<uuid:pk>/reviews/', ProductReviewsView.as_view(), name='product_reviews'),

    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/items/<uuid:pk>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/remove/<uuid:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
    
    # Orders
    path('orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('orders/<uuid:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/<uuid:pk>/status/', OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('orders/<uuid:pk>/cancel/', OrderCancelView.as_view(), name='order_cancel'),
    
    # Payment
    path('payment/process/', PaymentProcessView.as_view(), name='payment_process'),
    path('payment/<uuid:pk>/status/', PaymentStatusView.as_view(), name='payment_status'),
    
    # Delivery
    path('delivery/<uuid:pk>/status/', DeliveryStatusView.as_view(), name='delivery_status'),
    path('delivery/<uuid:pk>/update/', DeliveryUpdateView.as_view(), name='delivery_update'),
    
    # Reviews
    path('reviews/', ReviewListCreateView.as_view(), name='review_list_create'),
    path('reviews/<uuid:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    
    # Wishlist
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<uuid:pk>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    
    # Coupons
    path('coupons/', CouponListView.as_view(), name='coupon_list'),
    path('coupons/validate/', CouponValidateView.as_view(), name='coupon_validate'),
    path('coupons/apply/', ApplyCouponView.as_view(), name='coupon_apply'),
    
    # Analytics
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('reports/sales/', SalesReportView.as_view(), name='sales_report'),
]