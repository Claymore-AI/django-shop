# shop/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartItemSerializer


def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# --- Каталог ---
class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer


# --- Кошик ---
class CartAPI(APIView):
    def get(self, request):
        cart = get_cart(request)
        items = cart.items.select_related("product", "product__category")
        serializer = CartItemSerializer(items, many=True)
        return Response({
            "items": serializer.data,
            "total": cart.total_price()
        })

    def post(self, request):
        cart = get_cart(request)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = quantity
        item.save()

        return Response({"message": "Item added/updated"}, status=status.HTTP_200_OK)

    def delete(self, request):
        cart = get_cart(request)
        product_id = request.data.get("product_id")
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.delete()
        return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)
