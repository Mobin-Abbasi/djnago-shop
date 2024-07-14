from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
import random

from .forms import PhoneVerificationForm
from account.models import ShopUser
from cart.common.KaveSms import send_sms_with_template, send_sms_normal

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
                send_sms_normal('phone', 'به نمیدونم کجا خوش امدید')
                print(user)
                login(request, user)
                del request.session['verification_code']
                del request.session['phone']

            else:
                messages.error(request, 'Verification code is incorrect')

    return render(request, 'verify_code.html')