from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import CustomerSerializer

from django.contrib.auth import get_user_model


from .models import Product
from .serializers import ProductSerializer

from .models import Category
from .serializers import CategorySerializer


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

