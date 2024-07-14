from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
import random
from django.contrib.auth.decorators import login_required

from .forms import PhoneVerificationForm, OrderCreateForm
from account.models import ShopUser
from cart.common.KaveSms import send_sms_with_template, send_sms_normal
from .models import OrderItem
from cart.cart import Cart

# Create your views here.


def verify_phone(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                messages.error(request, 'this phone is already registered')
                return redirect('orders:verify_phone')
            else:
                tokens = {'token': ''.join(random.choices('123456789', k=4))}
                request.session['verification_code'] = tokens['token']
                request.session['phone'] = phone
                print(tokens)
                send_sms_with_template(phone, tokens, 'verify')
                messages.error(request, 'verification code sent successfully')
                return redirect('orders:verify_code')
    else:
        form = PhoneVerificationForm()
    context = {
        'form': form,
    }
    return render(request, 'verify_phone.html', context)


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if code == verification_code:
                user = ShopUser.objects.create_users(phone=phone)
                user.set_password('123456')
                user.save()
                send_sms_normal('phone', 'به نمیدونم کجا خوش امدید')
                print(user)
                login(request, user)
                del request.session['verification_code']
                del request.session['phone']
                return redirect('orders:create_order')
            else:
                messages.error(request, 'Verification code is incorrect')

    return render(request, 'verify_code.html')


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
                                         price=item['price'], weight=item['weight'])
            cart.clear()
            return redirect('shop:product_list')
    else:
        form = OrderCreateForm()

    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'create_order.html', context)
