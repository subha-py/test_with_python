import sys
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages,auth
from accounts.models import Token
from django.core.urlresolvers import reverse
# Create your views here.
def send_login_email(request):
    email=request.POST.get('email')
    token=Token.objects.create(email=email)
    url=request.build_absolute_uri(
        reverse('login')+'?token={uid}'.format(uid=token.uid)
    )
    message_body='Use this link to log in\n\n:{url}'.format(url=url)
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email],
    )
    messages.success(request,'Check your email, we have sent you a link you can use to log in.')
    return redirect('/')

def login(request):
    user=auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request,user)
    return redirect('/')