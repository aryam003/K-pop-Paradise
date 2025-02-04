from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from . models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=uname
                return redirect(shop_home)
            else:
                req.session['user']=uname
                # return redirect(user_home)
        else:
            messages.warning(req,"invalid user or password")  
        return redirect(shop_login)
    else:      
        return render(req,'login.html')
    
def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)

# def register(req):
#     if req.method=='POST':
#         name=req.POST['name']
#         email=req.POST['email']
#         password=req.POST['password']
#         send_mail('Eshop registration', 'E_shop account created', settings.EMAIL_HOST_USER, [email])
#         try:
#             data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
#             data.save()
#             return redirect(shop_login)
#         except:
#             messages.warning(req,"user details already exits.")
#             return redirect(register)
#     else:
#         return render(req,'register.html')
def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits.")
            return redirect(register)
    else:
        return render(req,'register.html')

    




def shop_home(req):
    if 'shop' in req.session:
        bands=Band.objects.all()
        return render(req,'shop/home.html',{'bands':bands})
        # return render(req,'shop/shop_home.html')
    # else:
    #     return redirect(shop_login) 
    


def user_home(req):
    if 'user' in req.session:
        bands=Band.objects.all()
        return render(req,'user/home.html',{'bands':bands})
    

def concert_list(req, id):
    log_user = User.objects.get(username=req.session['user'])  
    band = Band.objects.get(id=id)  
    concerts = Concert.objects.filter(band=band) 
    return render(req, 'user/concert_list.html', {'band': band, 'concerts': concerts})



