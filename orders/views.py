from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
import random

from .forms import PhoneVerificationForm
from account.models import ShopUser
from cart.common.KaveSms import send_sms_with_template

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
                request.phone = phone
                print('tokens')
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
    pass