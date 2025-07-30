from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from apps.products.forms import ProductForm
from apps.products.models import Product
from apps.orders.models import Order, OrderItem

# Create your views here.
def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/products_list.html', {'products': products})

def search_products(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )[:5]
        results = [
            {
                'id': p.id,
                'name': p.name,
                'image': p.image.url if p.image else '',
                'price': str(p.price),
                'category': p.category.name if p.category else ''
            } for p in products
        ]
    return JsonResponse(results, safe=False)

def search_results(request):
    query = request.GET.get('q', '')
    products = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'products/search_results.html', {'products': products, 'query': query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def is_seller(user):
    return user.is_authenticated and user.role == 'seller'

@login_required
@user_passes_test(is_seller)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'Added {product.name} to cart!')
    return redirect('product_detail', pk=pk)

def view_cart(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'products/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def buy_cart(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('view_cart')
    products = Product.objects.filter(id__in=cart.keys())
    total = 0
    eco_points_earned = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        total += product.price * quantity
        eco_points_earned += product.eco_points * quantity
    order = Order.objects.create(
        user=request.user,
        order_date=timezone.now(),
        status='pending',
        total=total
    )
    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity > 0:
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
    request.user.eco_points += eco_points_earned
    request.user.save()
    request.session['cart'] = {}
    messages.success(request, f'Order placed successfully! You earned {eco_points_earned} eco points!')
    return redirect('my_orders')

@login_required
@user_passes_test(is_seller)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'products/delete_product_confirm.html', {'product': product})

