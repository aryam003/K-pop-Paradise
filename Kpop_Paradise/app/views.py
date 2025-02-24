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
from django.template.loader import render_to_string  # For rendering email content
from django.core.mail import EmailMessage
from django.utils.html import strip_tags 

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
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        
        if not name or not email or not password:
            messages.warning(req, "All fields are required.")
            return redirect(register)
        
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.warning(req, "Please enter a valid email address.")
            return redirect(register)
        
        if len(password) < 8:
            messages.warning(req, "Password must be at least 8 characters long.")
            return redirect(register)

        if User.objects.filter(email=email).exists():
            messages.warning(req, "User with this email already exists.")
            return redirect(register)

        try:
            # Create the user
            data = User.objects.create_user(first_name=name, username=email, email=email, password=password)
            data.save()

            # Send confirmation email
            subject = 'Registration Successful'
            message = f'Hello {name},\n\nThank you for registering on our platform.\n\nBest regards,\nYour Company Name'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)

            messages.success(req, "Registration successful! A confirmation email has been sent.")
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
    log_user = User.objects.get(username=req.session['user']) 
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
        # Fetch the user profile if the user is authenticated
        user = request.user if request.user.is_authenticated else None
        if user:
            user_profile = UserProfile.objects.get(user=user)
            buyer_name = user_profile.name if user_profile.name else ''
            email = user.email
        else:
            # Fallback for guests (if not logged in)
            buyer_name = request.POST.get("name")
            email = request.POST.get("email")
        
        # Check for valid name and email for guests
        if not user and (not buyer_name or not email):
            messages.error(request, 'You must provide your name and email.')
            return redirect(book_ticket, concert_id=concert_id)

        quantity = int(request.POST.get("quantity"))
        total_price = concert.price * quantity
        
        ticket = Ticket.objects.create(
            concert=concert,
            user=user,  # Attach the user if authenticated
            buyer_name=buyer_name,
            email=email,
            quantity=quantity,
            total_price=total_price
        )

        # Email setup
        subject = f"Your Ticket for {concert.band.name} Concert"
        html_message = render_to_string('user/ticket_email.html', {
            'buyer_name': buyer_name,
            'concert': concert,
            'quantity': quantity,
            'total_price': total_price,
        })

        concert_image_path = concert.image.path 
        email_message = EmailMessage(
            subject=subject,
            body=strip_tags(html_message),  
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        with open(concert_image_path, 'rb') as img_file:
            email_message.attach(
                'concert_image.jpg', 
                img_file.read(), 
                'image/jpeg'  
            )
        
        cid = 'concert_image' 
        html_message_with_image = html_message.replace(
            'concert_image.jpg', f'cid:{cid}' 
        )
        email_message.content_subtype = 'html'
        email_message.body = html_message_with_image

        email_message.send()
        messages.success(request, f"Ticket booked successfully! A confirmation email has been sent to {email}. Total price: {total_price:.2f}")
        return redirect(user_home)

    return render(request, 'user/book_ticket.html', {'concert': concert})




# def user_view_bookings(req):
# user=User.objects.get(username=request.session['user'])
#     data=Ticket.objects.filter(user=user)
#     return render(req,'user/view_booking.html',{'data':data})


def user_tickets(request):
    if 'user'in request.session:
        # return redirect('login')  
        user = User.objects.get(username=request.session['user'])
        tickets = Ticket.objects.filter(user=user).order_by('-id') 
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
      
        buyer_name = request.POST.get('buyer_name', '')
        email = request.POST.get('email', '')
        if not user and (not buyer_name or not email):
            messages.error(request, 'You must provide your name and email.')
            return redirect(buy_product, product_id=product_id)
        booking = Booking.objects.create(
            product=product,
            user=user,
            buyer_name=buyer_name,
            email=email)
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

def checkout_cart(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect(cart_view)
        
        for item in cart_items:
            Booking.objects.create(
                product=item.product,
                user=request.user,
                # buyer_name=request.user.name,
                email=request.user.email
            )
            item.delete()
        messages.success(request, 'Your order has been placed successfully!')
        return redirect(user_home) 
    
    return redirect(cart_view)

def delete_cart(req, id):
    cart_item=Cart.objects.get(pk=id)
    cart_item.delete()  
    return redirect(cart_view)


def view_bookings(request):
    # Get current time and one day ago
    now = timezone.now()
    now_minus_one_day = now - timedelta(days=1)

    # Fetch bookings for the user
    bookings = Booking.objects.filter(user=request.user)

    # Pass the time calculated in the view
    return render(request, 'user/view_pro_booking.html', {
        'bookings': bookings,
        'now_minus_one_day': now_minus_one_day
    })

from datetime import timedelta

def delete_booking(request, booking_id):
    # Get the booking by id
    booking = Booking.objects.get( id=booking_id)
    # product = products.objects.get(id=product_id)  

    # Check if the booking is made within the last 24 hours
    if booking.booking_date > timezone.now() - timedelta(days=1):
        booking.delete()
    
    # Redirect the user back to their bookings page
    return redirect('view_bookings') # Redirect back to the bookings page

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


