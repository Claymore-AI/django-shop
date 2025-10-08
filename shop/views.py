from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Product, Cart, CartItem

class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 6  # можна змінити на будь-яке число

    def get_queryset(self):
        queryset = Product.objects.all().select_related("category")
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_category"] = self.request.GET.get("category")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

def get_cart(request):
    """Отримати або створити кошик за session_key"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


@require_POST
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect("shop:cart_view")


def cart_view(request):
    cart = get_cart(request)
    items = cart.items.select_related("product")
    total = cart.total_price()
    return render(request, "shop/cart.html", {"cart": cart, "items": items, "total": total})


@require_POST
@transaction.atomic
def update_cart_item(request, item_id):
    """Оновлення кількості товару"""
    item = get_object_or_404(CartItem, id=item_id, cart__session_key=request.session.session_key)
    quantity = int(request.POST.get("quantity", 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect("shop:cart_view")


@require_POST
def remove_from_cart(request, item_id):
    """Видалення товару з кошика"""
    item = get_object_or_404(CartItem, id=item_id, cart__session_key=request.session.session_key)
    item.delete()
    return redirect("shop:cart_view")