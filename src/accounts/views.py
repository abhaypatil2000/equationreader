from django.shortcuts import render , redirect

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from .models import Profile, User
import random

import http.client
import requests

from django.conf import settings
from django.contrib.auth import authenticate, login

# Create your views here.


def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=Here%20is%20your%20OTP%20for%20BlindRead%20"+ otp + "&language=english&route=p&numbers="+mobile
    headers = {
        'authorization': "SHiz8hcE1IqksePRrNUfvj35AVodQyZmaCYTWFtxpMJ42X06KBO1LokJ7PWD5bxRtIC3zrHqnavNflEY",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response)
    return None



def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        
        user = Profile.objects.filter(mobile = mobile).first()
        
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'accounts/login.html' , context)
        
        otp = str(random.randint(1000 , 9999))
        user.otp = otp
        print(otp)
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('accounts:login_otp')        
    return render(request,'accounts/login.html')


def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if otp == profile.otp:
            user = User.objects.get(id = profile.user.id)
            login(request , user)
            return redirect('home')
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'accounts/login_otp.html' , context)
    
    return render(request,'accounts/login_otp.html' , context)
    
    

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        
        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        
        if check_user or check_profile:
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'accounts/register.html' , context)
            
        user = User(email = email , first_name = name)
        user.save()
        otp = str(random.randint(1000 , 9999))
        profile = Profile(user = user , mobile=mobile , otp = otp) 
        profile.save()
        send_otp(mobile, otp)
        print(otp)
        request.session['mobile'] = mobile
        return redirect('accounts:otp')
    return render(request,'accounts/register.html')

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        if otp == profile.otp:
            return redirect('home')
        else:
            print('Wrong')
            
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'accounts/otp.html' , context)
            
        
    return render(request,'accounts/otp.html' , context)