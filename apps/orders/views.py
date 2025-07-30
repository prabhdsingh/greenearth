from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order

# Create your views here.

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date').prefetch_related('items__product')
    return render(request, 'orders/my_orders.html', {'orders': orders})

def order_list(request):
    orders = Order.objects.all().order_by('-order_date').prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})
