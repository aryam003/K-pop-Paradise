from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from . models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


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

# def register(req):
#     if req.method=='POST':
#         name=req.POST['name']
#         email=req.POST['email']
#         password=req.POST['password']
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
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        # password_confirm = req.POST['password_confirm']  # If you have a confirm password field

        # Validation for empty fields
        if not name or not email or not password:
            messages.warning(req, "All fields are required.")
            return redirect(register)

        # Validate email format
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.warning(req, "Please enter a valid email address.")
            return redirect(register)

        # Validate password length and strength
        if len(password) < 8:
            messages.warning(req, "Password must be at least 8 characters long.")
            return redirect(register)

        # Check if passwords match (if you have a confirmation password field)
        # if password != password_confirm:
        #     messages.warning(req, "Passwords do not match.")
        #     return redirect(register)

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(req, "User with this email already exists.")
            return redirect(register)

        try:
            # Create the user
            data = User.objects.create_user(first_name=name, username=email, email=email, password=password)
            data.save()
            return redirect(shop_login)  # Assuming shop_login is the login view
        except Exception as e:
            # Catch unexpected errors
            messages.warning(req, f"Error: {str(e)}")
            return redirect(register)

    else:
        return render(req, 'register.html')

    
#----SHOP-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def shop_home(req):
    if 'shop' in req.session:
        bands=Band.objects.all()
        return render(req,'shop/home.html',{'bands':bands})
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

def booking_list(request):
    # Fetch all bookings from the database, ordered by the most recent
    bookings = Booking.objects.all().order_by('-booking_date')

    # Pass the bookings to the template
    return render(request, 'shop/booking_list.html', {'bookings': bookings})


#-----USER---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    


def user_home(req):
    if 'user' in req.session:
        bands=Band.objects.all()
        return render(req,'user/home.html',{'bands':bands})
    else:
        return redirect(shop_login) 
    

def concert_list(req, id):
    log_user = User.objects.get(username=req.session['user'])  
    band = Band.objects.get(pk=id)  
    concerts = Concert.objects.filter(band=band) 
    product = products.objects.filter(band=band)
    return render(req, 'user/concert_list.html', {'band': band, 'concerts': concerts, 'products': product})



def book_ticket(request, concert_id):
    concert = Concert.objects.get(id=concert_id)
    if request.method == "POST":
        buyer_name = request.POST.get("name")
        email = request.POST.get("email")
        quantity = int(request.POST.get("quantity")) 
        total_price = concert.price * quantity

        Ticket.objects.create(
            concert=concert, 
            buyer_name=buyer_name, 
            email=email, 
            quantity=quantity,
            total_price=total_price
        )
        messages.success(request, f"Ticket booked successfully! Total price: {total_price:.2f}")
        return redirect(user_home)

    return render(request, 'user/book_ticket.html', {'concert': concert})

# def user_view_bookings(req):
# user=User.objects.get(username=request.session['user'])
#     data=Ticket.objects.filter(user=user)
#     return render(req,'user/view_booking.html',{'data':data})


def user_tickets(request):
    user=User.objects.get(username=request.session['user'])
    tickets = Ticket.objects.filter(user=request.user) [::-1]
    return render(request, 'user/user_tickets.html', {'tickets': tickets})



#---------------------------------------------------------------------------------PRODUCTS


def product_detail(req, product_id):
    product = products.objects.get(id=product_id)
    product_in_cart = Cart.objects.filter(user=req.user, product=product).exists() if req.user.is_authenticated else False
    return render(req, 'user/product_detail.html', {'product': product, 'product_in_cart': product_in_cart})



def buy_product(request, product_id):
    product = products.objects.get(id=product_id)
    
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        
        # Fetch user profile if the user is authenticated
        if user:
            user_profile = UserProfile.objects.get(user=user)
            buyer_name = user_profile.name if user_profile.name else ''
            email = user.email  # You can use the email from the User model
        else:
            # If not authenticated, fetch name and email from POST data
            buyer_name = request.POST.get('buyer_name', '')
            email = request.POST.get('email', '')
        
        # Check if either user is not authenticated or buyer details are missing
        if not user and (not buyer_name or not email):
            messages.error(request, 'You must provide your name and email.')
            return redirect(buy_product, product_id=product_id)

        # Create a booking with the gathered details
        booking = Booking.objects.create(
            product=product,
            user=user,
            buyer_name=buyer_name,
            email=email
        )
        
        messages.success(request, f'You have successfully booked the {product.name}!')
        return redirect(product_detail, product_id=product_id)
    
    return render(request, 'user/book_product.html', {'product': product})



def add_to_cart(req, product_id):
    product = products.objects.get(id=product_id)  
    cart_item, created = Cart.objects.get_or_create(user=req.user, product=product)
    if not created:  
        cart_item.quantity += 1
        cart_item.save()
    return redirect(user_home)

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'user/user_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def delete_cart(req, id):
    cart_item=Cart.objects.get(pk=id)
    cart_item.delete()  
    return redirect(cart_view)

def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user/view_pro_booking.html', {'bookings': bookings})


def ticket_booking_details(request):
    tickets = Ticket.objects.select_related('concert', 'user').all()
    return render(request, 'shop/booking_details.html', {'tickets': tickets})




def about(req):
    return render(req,'user/about.html')

# ---------------------User profile----------------------------------------------------------------------------------------------------------------


def user_profile(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    tickets = Ticket.objects.filter(user=user)
    bookings = Booking.objects.filter(user=user)
    return render(request, 'user/profile.html', {'profile': profile,'tickets': tickets,'bookings': bookings,})


def add_edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        profile.name = request.POST.get('name', profile.name) 
        profile.bio = request.POST.get('bio', profile.bio)

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()  
        return redirect('user_profile') 
    return render(request, 'user/add_edit_profile.html', {'profile': profile})


