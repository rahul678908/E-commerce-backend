from django.urls import path
from .views import *

urlpatterns = [
    path('superadmin/login/', SuperAdminLoginView.as_view(), name='superadmin-login'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-rud'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-rud'),

    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand-rud'),

    path('variants/', ProductVariantListCreateView.as_view(), name='variants'),
    path('variants/<str:sku>/', ProductVariantDetailView.as_view(), name='variant-detail'),

    path('cart-items/', CartItemListCreateView.as_view(), name='cart-item-list-create'),
    path('cart-items/<int:pk>/', CartView.as_view(), name='cart-item-rud'),

    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand-rud'),

    path('wishlists/', WishlistListCreateView.as_view(), name='wishlist-list-create'),

    path('coupons/', CouponListCreateView.as_view(), name='coupon-list-create'),

    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),

    path('address/', AddressListCreateView.as_view(), name='address-list-create'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('payments/', PaymentListView.as_view(), name='payment-list')
]