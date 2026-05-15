from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import Category

from rest_framework import serializers

from .models import (
    Product,
    ProductVariant,
    ProductImage,
    Category,
    Brand,
    ProductVariant,
    Address,
    Cart,
    CartItem,
    Wishlist,
    Coupon,
    Order,
    OrderItem,
    Payment,
    Review,
)



class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Review

        fields = [
            'id',
            'product',
            'username',
            'rating',
            'review',
            'created_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment

        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order

        fields = '__all__'

        read_only_fields = [
            'user',
            'order_number',
            'payment_status',
            'order_status'
        ]


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon

        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = Wishlist

        fields = [
            'id',
            'product',
            'product_name',
            'created_at'
        ]


class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='variant.product.name',
        read_only=True
    )

    class Meta:
        model = CartItem

        fields = [
            'id',
            'cart',
            'variant',
            'product_name',
            'quantity',
            'created_at'
        ]


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart

        fields = [
            'id',
            'user',
            'created_at'
        ]

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address

        fields = [
            'id',
            'user',
            'full_name',
            'phone',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'postal_code',
            'address_type',
            'is_default',
            'created_at'
        ]

        read_only_fields = ['user']


class ProductVariantSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = ProductVariant

        fields = [
            'id',
            'product',
            'product_name',
            'sku',
            'barcode',
            'price',
            'sale_price',
            'cost_price',
            'stock',
            'low_stock_threshold',
            'weight',
            'length',
            'width',
            'height',
            'tax_percentage',
            'is_default',
            'is_active',
            'created_at',
        ]

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand

        fields = [
            'id',
            'name',
            'slug',
            'logo',
            'description',
            'is_active',
            'created_at',
        ]


class CategorySerializer(serializers.ModelSerializer):

    parent_name = serializers.CharField(
        source='parent.name',
        read_only=True
    )

    class Meta:
        model = Category

        fields = [
            'id',
            'name',
            'slug',
            'parent',
            'parent_name',
            'image',
            'description',
            'meta_title',
            'meta_description',
            'is_active',
            'created_at',
        ]



class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = [
            'id',
            'image',
            'is_primary'
        ]




class ProductVariantSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ProductVariant

        fields = [
            'id',
            'sku',
            'price',
            'sale_price',
            'stock',
            'images'
        ]




class ProductSerializer(serializers.ModelSerializer):

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    brand_name = serializers.CharField(
        source='brand.name',
        read_only=True
    )

    class Meta:
        model = Product

        fields = [
            'id',
            'name',
            'slug',
            'thumbnail',
            'category',
            'category_name',
            'brand',
            'brand_name',
            'short_description',
            'description',
            'variants'
        ]

User = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            'id',
            'username',
            'email',
            'role',
            'phone',
            'date_joined',
        )

        read_only_fields = (
            'id',
            'date_joined',
        )

