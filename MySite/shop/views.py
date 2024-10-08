from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Product, Comment, Cart
from .serializers import ProductSerializer, CommentSerializer, CartSerializer, FindProductToCartSerializer
from .services import update_product_rating, get_cart, add_to_cart, remove_from_cart


class ProductListCreateView(APIView):
    """View for listing and creating products."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve a list of all products."""
        paginator = PageNumberPagination()
        products = Product.objects.all()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Create a new product."""
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            response_data = {
                "message": "Product created successfully.",
                "product": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """View for retrieving and updating a specific product."""

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        """Retrieve a product by its slug."""
        product = get_object_or_404(Product, slug=slug)
        update_product_rating(product)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        """Update a product by its slug."""
        product = get_object_or_404(Product, slug=slug)

        if product.author != request.user:
            return Response({"detail": "You do not have permission to update this product."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(product, data=request.data, partial=True, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Product updated successfully.",
                "product": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCommentsView(APIView):
    """View for retrieving and creating comments for a product."""

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        """Retrieve all comments for a specific product."""
        product = get_object_or_404(Product, slug=slug)
        comments = product.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        """Create a new comment for a specific product."""
        product = get_object_or_404(Product, slug=slug)
        serializer = CommentSerializer(data=request.data, context={"request": request, "product": product})

        if serializer.is_valid():
            comment = serializer.save()
            data = {
                "message": "Comment created successfully.",
                "product": CommentSerializer(comment).data,
                "product_slug": product.slug
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    """API view for managing user cart."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the user's cart data."""
        data = get_cart(request)
        return Response(data)

    def post(self, request):
        """Add a product to the user's cart."""
        serializer = FindProductToCartSerializer(data=request.data)
        if serializer.is_valid():
            data = add_to_cart(request, serializer)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Remove a product from the user's cart."""
        serializer = FindProductToCartSerializer(data=request.data)
        if serializer.is_valid():
            data = remove_from_cart(request, serializer)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
