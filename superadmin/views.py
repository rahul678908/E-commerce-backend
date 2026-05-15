from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import CustomerSerializer, ProductVariantSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
import uuid

from django.db import transaction

from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)

from .models import (
        Product,
        ProductVariant,
        Category,
        Brand,
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

from .serializers import (
        ProductSerializer,
        ProductVariantSerializer,
        CategorySerializer,
        BrandSerializer,
        AddressSerializer,
        CartSerializer,
        CartItemSerializer,
        WishlistSerializer,
        CouponSerializer,
        OrderSerializer,
        OrderItemSerializer,
        PaymentSerializer,
        ReviewSerializer,
)


class ReviewListCreateView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        product_id = request.query_params.get('product')

        reviews = Review.objects.select_related(
            'user',
            'product'
        ).filter(product_id=product_id)

        serializer = ReviewSerializer(
            reviews,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = ReviewSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response({
                'message': 'Review added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PaymentListView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        payments = Payment.objects.filter(
            order__user=request.user
        )

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(serializer.data)


class OrderItemListView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        order_items = OrderItem.objects.select_related(
            'order',
            'variant'
        ).filter(order__user=request.user)

        serializer = OrderItemSerializer(
            order_items,
            many=True
        )

        return Response(serializer.data)



class OrderListCreateView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        orders = Order.objects.filter(
            user=request.user
        )

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)


    @transaction.atomic
    def post(self, request):

        serializer = OrderSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user,
                order_number=str(uuid.uuid4())[:12]
            )

            return Response({
                'message': 'Order created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CouponListCreateView(APIView):

    permission_classes = [IsAdminUser]


    def get(self, request):

        coupons = Coupon.objects.all()

        serializer = CouponSerializer(
            coupons,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = CouponSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Coupon created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class WishlistListCreateView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        wishlist = Wishlist.objects.select_related(
            'product'
        ).filter(user=request.user)

        serializer = WishlistSerializer(
            wishlist,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = WishlistSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response({
                'message': 'Added to wishlist',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CartItemListCreateView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_items = CartItem.objects.select_related(
            'variant',
            'variant__product'
        ).filter(cart=cart)

        serializer = CartItemSerializer(
            cart_items,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        serializer = CartItemSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(cart=cart)

            return Response({
                'message': 'Item added to cart',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CartView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        serializer = CartSerializer(cart)

        return Response(serializer.data)
    


class AddressListCreateView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        addresses = Address.objects.filter(
            user=request.user
        )

        serializer = AddressSerializer(
            addresses,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = AddressSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response({
                'message': 'Address created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class ProductVariantDetailView(APIView):


    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        if self.request.method == 'GET':
            return []

        return [IsAdminUser()]


    # SINGLE VARIANT
    def get(self, request, sku):

        try:

            variant = ProductVariant.objects.select_related(
                'product'
            ).get(sku=sku)

        except ProductVariant.DoesNotExist:

            return Response({
                'error': 'Variant not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductVariantSerializer(variant)

        return Response(serializer.data)


    # UPDATE VARIANT
    def put(self, request, sku):

        try:

            variant = ProductVariant.objects.get(sku=sku)

        except ProductVariant.DoesNotExist:

            return Response({
                'error': 'Variant not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductVariantSerializer(
            variant,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Variant updated successfully',
                'data': serializer.data
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # DELETE VARIANT
    def delete(self, request, sku):

        try:

            variant = ProductVariant.objects.get(sku=sku)

        except ProductVariant.DoesNotExist:

            return Response({
                'error': 'Variant not found'
            }, status=status.HTTP_404_NOT_FOUND)

        variant.delete()

        return Response({
            'message': 'Variant deleted successfully'
        })


# VARIANT LIST + CREATE
class ProductVariantListCreateView(APIView):


    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        if self.request.method == 'GET':
            return []

        return [IsAdminUser()]


    # GET VARIANTS
    def get(self, request):

        variants = ProductVariant.objects.select_related(
            'product'
        ).all()

        serializer = ProductVariantSerializer(
            variants,
            many=True
        )

        return Response(serializer.data)


    # CREATE VARIANT
    def post(self, request):

        serializer = ProductVariantSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Variant created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
# BRAND LIST + CREATE
class BrandListCreateView(APIView):

    parser_classes = (
        MultiPartParser,
        FormParser
    )


    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        # PUBLIC ACCESS FOR GET
        if self.request.method == 'GET':
            return []

        # ADMIN ACCESS FOR POST
        return [IsAdminUser()]


    # GET ALL BRANDS
    def get(self, request):

        brands = Brand.objects.all()

        serializer = BrandSerializer(
            brands,
            many=True
        )

        return Response(serializer.data)


    # CREATE BRAND
    def post(self, request):

        serializer = BrandSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Brand created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# BRAND DETAILS
class BrandDetailView(APIView):

    parser_classes = (
        MultiPartParser,
        FormParser
    )


    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        # PUBLIC ACCESS FOR GET
        if self.request.method == 'GET':
            return []

        # ADMIN ACCESS FOR PUT & DELETE
        return [IsAdminUser()]


    # GET SINGLE BRAND
    def get(self, request, slug):

        try:

            brand = Brand.objects.get(slug=slug)

        except Brand.DoesNotExist:

            return Response({
                'error': 'Brand not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BrandSerializer(brand)

        return Response(serializer.data)


    # UPDATE BRAND
    def put(self, request, slug):

        try:

            brand = Brand.objects.get(slug=slug)

        except Brand.DoesNotExist:

            return Response({
                'error': 'Brand not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BrandSerializer(
            brand,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Brand updated successfully',
                'data': serializer.data
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # DELETE BRAND
    def delete(self, request, slug):

        try:

            brand = Brand.objects.get(slug=slug)

        except Brand.DoesNotExist:

            return Response({
                'error': 'Brand not found'
            }, status=status.HTTP_404_NOT_FOUND)

        brand.delete()

        return Response({
            'message': 'Brand deleted successfully'
        })

# CATEGORY LIST + CREATE
class CategoryListCreateView(APIView):


    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        # PUBLIC ACCESS FOR GET
        if self.request.method == 'GET':
            return []

        # ADMIN ACCESS FOR POST
        return [IsAdminUser()]


    # GET ALL CATEGORIES
    def get(self, request):

        categories = Category.objects.select_related(
            'parent'
        ).all()

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)


    # CREATE CATEGORY
    def post(self, request):

        serializer = CategorySerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Category created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# CATEGORY DETAILS
class CategoryDetailView(APIView):


    # DYNAMIC PERMISSIONS
    def get_permissions(self):

        # PUBLIC ACCESS FOR GET
        if self.request.method == 'GET':
            return []

        # ADMIN ACCESS FOR UPDATE & DELETE
        return [IsAdminUser()]


    # SINGLE CATEGORY
    def get(self, request, slug):

        try:

            category = Category.objects.select_related(
                'parent'
            ).get(slug=slug)

        except Category.DoesNotExist:

            return Response({
                'error': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)

        return Response(serializer.data)


    # UPDATE CATEGORY
    def put(self, request, slug):

        try:

            category = Category.objects.get(slug=slug)

        except Category.DoesNotExist:

            return Response({
                'error': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Category updated successfully',
                'data': serializer.data
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # DELETE CATEGORY
    def delete(self, request, slug):

        try:

            category = Category.objects.get(slug=slug)

        except Category.DoesNotExist:

            return Response({
                'error': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)

        category.delete()

        return Response({
            'message': 'Category deleted successfully'
        })

class ProductListCreateView(APIView):

    # GET PRODUCTS
    def get(self, request):

        products = Product.objects.select_related(
            'category',
            'brand'
        ).prefetch_related(
            'variants',
            'variants__images'
        )

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)


    # CREATE PRODUCT
    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Product created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductDetailView(APIView):

    def get(self, request, pk):
        try:

            product = Product.objects.select_related(
                'category',
                'brand'
            ).prefetch_related(
                'variants',
                'variants__images'
            ).get(pk=pk)

        except Product.DoesNotExist:

            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    def put(self, request, pk):

        try:

            product = Product.objects.get(pk=pk)

        except Product.DoesNotExist:

            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                'message': 'Product updated successfully',
                'data': serializer.data
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:

            product = Product.objects.get(pk=pk)

        except Product.DoesNotExist:

            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)

        product.delete()

        return Response({
            'message': 'Product deleted successfully'
        })
        
# USER MODEL
User = get_user_model()


# CUSTOMER LIST VIEW
class CustomerListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        customers = User.objects.filter(
            is_superuser=False
        )

        serializer = CustomerSerializer(
            customers,
            many=True
        )

        return Response(serializer.data)
    

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# SUPER ADMIN LOGIN
class SuperAdminLoginView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:

            tokens = get_tokens_for_user(user)

            return Response({
                'message': 'Super admin login successful',
                'tokens': tokens,
                'user_id': user.id,
                'username': user.username,
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

