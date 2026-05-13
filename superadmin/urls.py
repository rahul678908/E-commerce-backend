from django.urls import path
from .views import *

urlpatterns = [
    path('superadmin/login/', SuperAdminLoginView.as_view(), name='superadmin-login'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-rud'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-rud'),
]