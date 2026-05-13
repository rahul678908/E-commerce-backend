from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import Category

from rest_framework import serializers

from .models import (
    Product,
    ProductVariant,
    ProductImage,
    Category,
)




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

