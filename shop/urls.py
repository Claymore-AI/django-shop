from django.urls import path
from . import views, api_views

app_name = "shop"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),

    # API частина
    path("api/products/", api_views.ProductListAPI.as_view(), name="api_products"),
    path("api/products/<int:pk>/", api_views.ProductDetailAPI.as_view(), name="api_product_detail"),
    path("api/cart/", api_views.CartAPI.as_view(), name="api_cart"),
]