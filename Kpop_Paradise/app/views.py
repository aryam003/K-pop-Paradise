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
                return redirect(user_home)
        else:
            messages.warning(req,"invalid user or password")  
        return redirect(shop_login)
    else:      
        return render(req,'login.html')
    
def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)

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

    
#----SHOP-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def shop_home(req):
    if 'shop' in req.session:
        bands=Band.objects.all()
        return render(req,'shop/home.html',{'bands':bands})
        # return render(req,'shop/shop_home.html')
    else:
        return redirect(shop_login) 
    
def shop_concert_list(req, id):
    # log_user = User.objects.get(username=req.session['user']) 
    band = Band.objects.get(id=id)  
    concerts = Concert.objects.filter(band=band) 
    product = products.objects.filter(band=band)
    return render(req, 'shop/concert_list.html', {'band': band, 'concerts': concerts , 'products': product})

def add_concert(req):
    if req.method == 'POST':
        artist = req.POST['artist']
        date = req.POST['date']
        location = req.POST['location']
        price = req.POST['price']
        total_ticket = req.POST['total_ticket']
        file = req.FILES.get('image')  
        band_id = req.POST['band_name']
        try:
            band = Band.objects.get(id=band_id)
        except Band.DoesNotExist:
            messages.error(req, "Band does not exist!")
            return redirect(add_concert)
        concert = Concert.objects.create(
            band=band,
            artist=artist, 
            date=date, 
            location=location, 
            price=price, 
            total_ticket=total_ticket, 
            image=file)
        concert.save()
        messages.success(req, "Concert added successfully!")
        return redirect(shop_home)
    bands = Band.objects.all()
    return render(req, 'shop/add_concert.html', {'bands': bands})


def edit_concert(req, id):
    concert = Concert.objects.get(pk=id) 
    if req.method == 'POST':
        artist = req.POST['artist']
        date = req.POST['date']
        location = req.POST['location']
        price = req.POST['price']
        band_id = req.POST['band_name']
        file = req.FILES.get('image') 
        try:
            band = Band.objects.get(id=band_id) 
        except Band.DoesNotExist:
            messages.error(req, "Band does not exist!")
            return redirect(edit_concert, id=id)
        concert.artist = artist
        concert.date = date
        concert.location = location
        concert.price = price
        concert.band = band
        if file:
            concert.image = file  
        concert.save()  
        messages.success(req, "Concert updated successfully!")
        return redirect(shop_home)  
    bands = Band.objects.all() 
    return render(req, 'shop/edit_concert.html', {'concert': concert, 'bands': bands})

def delete_concert(req, id):
    try:
        concert = Concert.objects.get(pk=id) 
        if concert.image:
            image_path = concert.image.path  
            if os.path.exists(image_path):
                os.remove(image_path)  
        concert.delete()  
        messages.success(req, "Concert deleted successfully!")
    except Concert.DoesNotExist:
        messages.error(req, "Concert not found!")
    
    return redirect(shop_home) 

def delete_product(req, id):
    try:
        product = products.objects.get(pk=id) 
        if product.image:
            image_path = product.image.path  
            if os.path.exists(image_path):
                os.remove(image_path)  
        product.delete()
        messages.success(req, "Product deleted successfully!")
    except products.DoesNotExist:
        messages.error(req, "Product not found!")
    return redirect(shop_home) 


#----------------------------------------------------------------------------Product
def add_product(req):
    if req.method == 'POST':
        name = req.POST['name']
        description = req.POST['description']
        price = req.POST['price']
        file = req.FILES.get('image') 
        band_id = req.POST['band_name']
        try:
            band = Band.objects.get(id=band_id)
        except Band.DoesNotExist:
            messages.error(req, "Band does not exist!")
            return redirect(add_product)
        product = products.objects.create(
            name=name, 
            description=description, 
            price=price, 
            image=file, 
            band=band)
        product.save()
        messages.success(req, "Product added successfully!")
        return redirect(shop_home)  
    bands = Band.objects.all()  
    return render(req, 'shop/add_product.html', {'bands': bands})



def edit_product(req, id):
    product = products.objects.get(pk=id)  
    if req.method == 'POST':
        name = req.POST['name']
        description = req.POST['description']
        price = req.POST['price']
        band_id = req.POST['band_name']
        file = req.FILES.get('image')  
        try:
            band = Band.objects.get(id=band_id)
        except Band.DoesNotExist:
            messages.error(req, "Band does not exist!")
            return redirect(edit_product, id=id)  
        if file:
            product.name = name
            product.description = description
            product.price = price
            product.band = band
            product.image = file
        else:
            product.name = name
            product.description = description
            product.price = price
            product.band = band
        product.save()      
        messages.success(req, "Product updated successfully!")
        return redirect(shop_home)  

    bands = Band.objects.all()  
    return render(req, 'shop/edit_product.html', {'product': product, 'bands': bands})

def delete_concert(req, id):
    try:
        concert = products.objects.get(pk=id) 
        if concert.image:
            image_path = concert.image.path  
            if os.path.exists(image_path):
                os.remove(image_path)  
        concert.delete()  
        messages.success(req, "Product deleted successfully!")
    except Concert.DoesNotExist:
        messages.error(req, "Product not found!")
    
    return redirect(shop_home) 


#-----USER---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    


def user_home(req):
    if 'user' in req.session:
        bands=Band.objects.all()
        return render(req,'user/home.html',{'bands':bands})
    else:
        return redirect(shop_login) 
    

def concert_list(req, id):
    # log_user = User.objects.get(username=req.session['user'])  
    band = Band.objects.get(pk=id)  
    concerts = Concert.objects.filter(band=band) 
    product = products.objects.filter(band=band)
    return render(req, 'user/concert_list.html', {'band': band, 'concerts': concerts, 'products': product})

def buy_ticket(req,id):
    concert = Concert.objects.get(id=id)
    return render(req,'user/user_dtls.html',{'concert':concert}) 






#---------------------------------------------------------------------------------PRODUCTS

def view_pro(req,id):
    log_user=User.objects.get(username=req.session['user'])
    product=products.objects.get(pk=id)
    try:
        cart=Cart.objects.get(product=product,user=log_user)
    except:
        cart=None
    return render(req,'user/view_pro.html',{'product':product,'cart':cart})

def cart_display(req):
    user = User.objects.get(username=req.session['user'])
    cart_items = Cart.objects.filter(user=user) 
    return render(req, 'shop/cart_display.html', {'cart_items': cart_items})


def add_to_cart(req, id):
    try:
        product = products.objects.get(pk=id)
    except products.DoesNotExist:
        messages.error(req, "Product not found!")
        return redirect('shop_home') 
    try:
        user = User.objects.get(username=req.session['user'])
    except User.DoesNotExist:
        messages.error(req, "User not found!")
        return redirect('login') 
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if created:
        messages.success(req, f"{product.name} added to your cart!")
    else:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(req, f"Quantity of {product.name} updated in your cart!")
    return redirect('cart_display') 

