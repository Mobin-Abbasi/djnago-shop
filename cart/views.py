from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from django.http import JsonResponse


# Create your views here.


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart':  cart
    }
    return render(request, 'cart/detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
        }
        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({'error': e})


@require_POST
def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)

        if action == 'add':
            cart.add(product)
        elif action == 'decrease':
            cart.decrease(product)

        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'success': True,
            'quantity': cart.cart[item_id]['quantity'],
            'total': cart.cart[item_id]['quantity'] * cart.cart[item_id]['price'],
            'final_price': cart.get_final_price(),

        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success': False, 'error': 'item not found'})


@require_POST
def remove_item(request):
    item_id = request.POST.get('item_id')
    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)
        cart.remove(product)

        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'success': True,
            'final_price': cart.get_final_price(),

        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success': False, 'error': 'item not found'})