from django.shortcuts import render,redirect,get_object_or_404
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
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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

# def booking_list(request):
#     # Fetch all bookings from the database, ordered by the most recent
#     bookings = Booking.objects.all().order_by('-booking_date')

#     # Pass the bookings to the template
#     return render(request, 'shop/booking_list.html', {'bookings': bookings})
 # Import necessary models

def booking_list(request):
    # Retrieve all concerts, tickets, orders, and purchases
    concerts = Concert.objects.all()
    tickets = Ticket.objects.select_related('concert', 'user').all()
    orders = Order.objects.select_related('concert', 'user').all()
    buys = Buy.objects.select_related('concert', 'user').all()

    context = {
        'concerts': concerts,
        'tickets': tickets,
        'orders': orders,
        'buys': buys,
    }

    return render(request, 'shop/booking_list.html', context)


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


def buy_pro(req, id):
    concert = Concert.objects.get(pk=id)
    return redirect(book_ticket, concert_id=id)
def book_ticket(req, concert_id):
    # Fetch the concert and user from the database
    concert = Concert.objects.get(id=concert_id)
    user = User.objects.get(username=req.session['user'])

    # Fetch the latest user address or None if no address exists
    user_address = Ticket.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        # Get form data
        name = req.POST.get('name')
        email = req.POST.get('email')
        quantity = int(req.POST.get("quantity"))
        total_price = concert.price * quantity

        # If user already has a ticket, update the ticket details
        if user_address:
            user_address.buyer_name = name
            user_address.email = email
            user_address.quantity = quantity
            user_address.total_price = total_price
            user_address.concert = concert  # Ensure the concert_id is set
            user_address.save()
        else:
            # Create a new ticket
            Ticket.objects.create(
                user=user,
                concert=concert,  # Assign the concert to the ticket
                buyer_name=name,
                email=email,
                quantity=quantity,
                total_price=total_price
            )

        # Email setup
        subject = f"Your Ticket for {concert.band.name} Concert"
        html_message = render_to_string('user/ticket_email.html', {
            'buyer_name': name,
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

        # Save the concert and quantity in the session for further use (like payment)
        req.session['concert'] = concert_id
        req.session['quantity'] = quantity

        # Success message and redirection
        messages.success(req, f"Ticket booked successfully! A confirmation email has been sent to {email}. Total price: {total_price:.2f}")
        return redirect(order_payment)

    # If not POST, just render the page with concert and user address details
    return render(req, 'user/book_ticket.html', {'concert': concert, 'user_address': user_address})

# def book_ticket(req, concert_id):
#     # Fetch the concert and user from the database
#     concert = Concert.objects.get(id=concert_id)
#     user = User.objects.get(username=req.session['user'])

#     # Fetch the latest user address or None if no address exists
#     user_address = Ticket.objects.filter(user=user).order_by('-id').first()

#     if req.method == 'POST':
#         # Get form data
#         name = req.POST.get('name')
#         email = req.POST.get('email')
#         quantity = int(req.POST.get("quantity"))
#         total_price = concert.price * quantity

#         # If user already has a ticket, update the ticket details
#         if user_address:
#             user_address.buyer_name = name
#             user_address.email = email
#             user_address.quantity = quantity
#             user_address.total_price = total_price
#             user_address.concert = concert  # Ensure the concert_id is set
#             user_address.save()
#         else:
#             # Create a new ticket
#             Ticket.objects.create(
#                 user=user,
#                 concert=concert,  # Assign the concert to the ticket
#                 buyer_name=name,
#                 email=email,
#                 quantity=quantity,
#                 total_price=total_price
#             )

#         # Save the concert and quantity in the session for further use (like payment)
#         req.session['concert'] = concert_id
#         req.session['quantity'] = quantity

#         # Redirect to the payment page
#         return redirect('order_payment')

#     # If not POST, just render the page with concert and user address details
#     return render(req, 'user/book_ticket.html', {'concert': concert, 'user_address': user_address})



@login_required
def order_payment(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        concert = Concert.objects.get(pk=req.session['concert'])
        quantity = req.session.get('quantity', 1)
        total_price = concert.price * quantity

        amount_in_paise = int(total_price * 100)
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        # razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = razorpay_client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": "1"
        })

        order = Order.objects.create(
            user=user,
            price=total_price,
            provider_order_id=razorpay_order['id']
        )

        req.session['order_id'] = order.pk

        return render(req, "user/payment.html", {
            "callback_url": "http://127.0.0.1:8000/callback/",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
        })

    return redirect(login)


@login_required
def pay(req):
    user = User.objects.get(username=req.session['user'])
    concert = Concert.objects.get(pk=req.session['concert'])

    if not concert:
        messages.error(req, "Your cart is empty. Please add a product first.")
        return redirect('user_home')

    order_id = req.session.get('order_id')
    order = get_object_or_404(Order, pk=order_id)

    if req.method == 'GET':
        user_address = Ticket.objects.filter(user=user).order_by('-id').first()

        if not user_address:
            messages.error(req, "No address found. Please add your address first.")
            return redirect(user_home)

        buy_data = Buy.objects.create(
            user=user,
            concert=concert,
            quantity=1,
            total_price=concert.price,
            order=order
        )
        messages.success(req, "Your order has been placed successfully.")
        return redirect(user_home)


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if verify_signature(request.POST):
            order.status = "SUCCESS"
            messages.success(request, "Payment successful!")
        else:
            order.status = "FAILURE"
            messages.error(request, "Payment verification failed. Please try again.")

        order.save()

        return redirect(pay)
    else:
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.status = "FAILURE"
        order.save()

        messages.error(request, "Payment failed. Please try again.")
        return redirect(pay)















# def book_ticket(request, concert_id):
#     concert = Concert.objects.get(id=concert_id)
    
#     if request.method == "POST":
#         # Fetch the user profile if the user is authenticated
#         user = request.user if request.user.is_authenticated else None
#         if user:
#             user_profile = UserProfile.objects.get(user=user)
#             buyer_name = user_profile.name if user_profile.name else ''
#             email = user.email
#         else:
#             # Fallback for guests (if not logged in)
#             buyer_name = request.POST.get("name")
#             email = request.POST.get("email")
        
#         # Check for valid name and email for guests
#         if not user and (not buyer_name or not email):
#             messages.error(request, 'You must provide your name and email.')
#             return redirect(book_ticket, concert_id=concert_id)

#         quantity = int(request.POST.get("quantity"))
#         total_price = concert.price * quantity
        
#         ticket = Ticket.objects.create(
#             concert=concert,
#             user=user,  # Attach the user if authenticated
#             buyer_name=buyer_name,
#             email=email,
#             quantity=quantity,
#             total_price=total_price
#         )

#         # Email setup
#         subject = f"Your Ticket for {concert.band.name} Concert"
#         html_message = render_to_string('user/ticket_email.html', {
#             'buyer_name': buyer_name,
#             'concert': concert,
#             'quantity': quantity,
#             'total_price': total_price,
#         })

#         concert_image_path = concert.image.path 
#         email_message = EmailMessage(
#             subject=subject,
#             body=strip_tags(html_message),  
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[email],
#         )
#         with open(concert_image_path, 'rb') as img_file:
#             email_message.attach(
#                 'concert_image.jpg', 
#                 img_file.read(), 
#                 'image/jpeg'  
#             )
        
#         cid = 'concert_image' 
#         html_message_with_image = html_message.replace(
#             'concert_image.jpg', f'cid:{cid}' 
#         )
#         email_message.content_subtype = 'html'
#         email_message.body = html_message_with_image

#         email_message.send()
#         messages.success(request, f"Ticket booked successfully! A confirmation email has been sent to {email}. Total price: {total_price:.2f}")
#         return redirect(user_home)

#     return render(request, 'user/book_ticket.html', {'concert': concert})




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

# def buy_product(request, product_id):
#     product = products.objects.get(id=product_id)
    
#     if request.method == 'POST':
#         user = request.user if request.user.is_authenticated else None
      
#         buyer_name = request.POST.get('buyer_name', '')
#         email = request.POST.get('email', '')
#         address = request.POST.get('address', '')
#         price = request.POST.get('price', '') 
#         if not user and (not buyer_name or not email):
#             messages.error(request, 'You must provide your name and email.')
#             return redirect(buy_product, product_id=product_id)
#         booking = Booking.objects.create(
#             product=product,
#             user=user,
#             buyer_name=buyer_name,
#             email=email,
#             address=address,
#             price=price)
#         messages.success(request, f'You have successfully booked the {product.name}!')
#         return redirect(product_detail, product_id=product_id)
    
#     return render(request, 'user/book_product.html', {'product': product})


def buy_pro2(req, id):
    product = products.objects.get(pk=id)
    return redirect(buy_product, id=id)  


def buy_product(req, product_id):
    product = products.objects.get(pk=product_id)
    user = User.objects.get(username=req.session['user'])  
    user_address = Booking.objects.filter(user=user).order_by('-id').first()

    if req.method == 'POST':
        user = req.user if req.user.is_authenticated else None

        buyer_name = req.POST.get('buyer_name', '')
        email = req.POST.get('email', '')
        address = req.POST.get('address', '') 
     
        if user_address:
            user_address.buyer_name = buyer_name
            user_address.address = address
            user_address.email = email
            user_address.save()
        else:
           data= Booking.objects.create(user=user, buyer_name=buyer_name, address=address, email=email)
        # data.save()
        req.session['product'] = product_id
        return redirect(order_payment2)  

    return render(req, 'user/book_product.html', {'product': product, 'user_address': user_address})



@login_required
def order_payment2(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])  
        product = products.objects.get(pk=req.session['product'])  
        amount = product.price 
        amount_in_paise = int(amount * 100)  

        print(f"Amount being passed to Razorpay (in paise): {amount_in_paise}")

        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        razorpay_order = razorpay_client.order.create({
            "amount": amount_in_paise,  
            "currency": "INR",  
            "payment_capture": "1" 
        })

        order = Order2.objects.create(
            user=user,
            price=amount, 
            product=product,
            provider_order_id=razorpay_order['id']  
        )
        req.session['order_id'] = order.pk  

        return render(req, "user/payment.html", {
            "callback_url": "http://127.0.0.1:8000/callback2/", 
            "razorpay_key": settings.RAZORPAY_KEY_ID, 
            "order": order,  
        })
    return redirect(login)  


# @login_required
# def pay2(req):
#     user = User.objects.get(username=req.session['user'])  
#     product = products.objects.get(pk=req.session['product'])

#     if not product:
#         messages.error(req, "Your cart is empty. Please add a product first.")
#         return redirect(cart_view)

#     order_id = req.session.get('order_id')
#     order = get_object_or_404(Order2, pk=order_id) if order_id else None

#     if req.method == 'GET':
#         user_address = Booking.objects.filter(user=user).order_by('-id').first()
#         # booking = Booking.objects.get(id=26)
#         # buy2 = Buy2.objects.create(address=booking)
#         data = Buy2.objects.create(
#             user=user,
#             product=product,
#             price=product.price,
#             address=user_address,
#             email = user.email,
#             order=order
#         )
#         data.save()

#         return redirect(view_bookings)

#     return render(req, 'user/view_pro_booking.html')
@login_required
def pay2(req):
    user = User.objects.get(username=req.session['user'])  
    product = products.objects.get(pk=req.session['product'])

    if not product:
        messages.error(req, "Your cart is empty. Please add a product first.")
        return redirect(cart_view)

    order_id = req.session.get('order_id')
    order = get_object_or_404(Order2, pk=order_id) if order_id else None

    if req.method == 'GET':
        user_address = Booking.objects.filter(user=user).order_by('-id').first()
        if user_address:
            address_text = user_address.address  # Extract address as text
        else:
            address_text = ""  # Provide a fallback if no address is found

        data = Buy2.objects.create(
            user=user,
            product=product,
            price=product.price,
            address=address_text,  # Assign the address as text
            email=user.email,
            order=order
        )
        data.save()

        return redirect(view_bookings)

    return render(req, 'user/view_pro_booking.html')


@csrf_exempt
def callback2(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order2.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE

        order.save()
        return redirect(pay2)
    else:
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order2.objects.get(provider_order_id=provider_order_id)
        order.status = PaymentStatus.FAILURE
        order.save()

        return redirect(pay2)



def place_order2(req, id):
    product = products.objects.get(pk=id)
    user = req.user
    # size = req.POST.get('size', 10)  
    data = Buy2.objects.create(
        user=user, 
        product=product, 
        price=product.price,
        address=None,  
        is_confirmed=False,
    )
    data.save()

    return redirect(user_home) 

















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

# def ticket_booking_details(request):
#     tickets = Ticket.objects.select_related('concert', 'user').all()
#     return render(request, 'shop/booking_details.html', {'tickets': tickets})
def ticket_booking_details(request):
    # Retrieve all bookings, orders, and purchases
    bookings = Booking.objects.select_related('product', 'user').all()
    orders = Order2.objects.select_related('product', 'user').all()
    buys = Buy2.objects.select_related('product', 'user').all()

    context = {
        'bookings': bookings,
        'orders': orders,
        'buys': buys,
    }

    return render(request, 'shop/booking_details.html', context)



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






def cart_address_page(req):
    user = User.objects.get(username=req.session['user'])  # Get the logged-in user
    
    # Retrieve the first booking address of the user (Booking is now assumed to be the address table)
    user_address = Booking.objects.filter(user=user).first()

    if req.method == 'POST':
        # Retrieve data from POST request
        name = req.POST.get('name')
        address = req.POST.get('address')
        phone_number = req.POST.get('phone_number')

        if user_address:
            # Update the user's saved address
            user_address.buyer_name = name
            user_address.address = address
            user_address.email = req.user.email  # Assuming email is the logged-in user's email
            user_address.price = 0.00  # Adjust according to the logic, here we're just setting a placeholder value
            user_address.save()
        else:
            # If no address exists, create a new one
            Booking.objects.create(user=user, buyer_name=name, address=address, phone_number=phone_number, email=req.user.email)

        # Get the user's cart items
        cart_items = Cart.objects.filter(user=user)

        # Iterate over the cart items to calculate the total price for each item
        for cart_item in cart_items:
            cart_item.total_price = cart_item.product.price * cart_item.quantity
        
        # Optionally, update session with cart items
        req.session['cart_items'] = list(cart_items.values_list('id', flat=True))

        # Redirect to the next step (for example: order_payment2)
        return redirect(order_payment3)

    return render(req, 'user/cart_order.html', {'user_address': user_address, 'cart_items': Cart.objects.filter(user=user)})


@login_required
def order_payment3(req):
    if 'user' in req.session:
        user = get_object_or_404(User, username=req.session['user'])
        cart_items = Cart.objects.filter(id__in=req.session.get('cart_items', []))

        if not cart_items.exists():
            return redirect('cart_display')

        # Calculate total amount
        total_amount = sum(cart.product.price * cart.quantity for cart in cart_items)

        # Razorpay API integration to create an order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            "amount": int(total_amount * 100),  # Razorpay expects the amount in paise (1 INR = 100 paise)
            "currency": "INR",
            "payment_capture": "1"
        })

        # For simplicity, assume we take the first product from the cart
        product = cart_items.first().product

        # Create an Order2 object
        order = Order2.objects.create(
            user=user,
            price=total_amount,
            provider_order_id=razorpay_order['id'],
            payment_id='',
            signature_id='',
            product=product  # Associate the product from the cart
        )

        # Store the order id in the session
        req.session['order_id'] = order.pk

        # Return the response with the Razorpay integration details
        return render(req, "user/payment.html", {
            "callback_url": "http://127.0.0.1:8000/callback2/",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
        })

    return redirect(login)


@login_required
def pay3(req):
    user = get_object_or_404(User, username=req.session['user'])
    cart_items = Cart.objects.filter(id__in=req.session.get('cart_items', []))

    if not cart_items.exists():
        messages.error(req, "Your cart is empty. Please add items first.")
        return redirect(cart_view)

    order_id = req.session.get('order_id')
    order = get_object_or_404(Order2, pk=order_id) if order_id else None

    user_address = Booking.objects.filter(user=user).order_by('-id').first()

    for cart in cart_items:
        Buy2.objects.create(
            user=user,
            product=cart.product,
            price=cart.product.price * cart.quantity,
            quantity=cart.quantity,
            address=user_address,
            order=order
        )

    cart_items.delete()

    return redirect(view_bookings)


@csrf_exempt
def callback3(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order2.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE

        order.save()
        
        # Create Buy2 objects for the order
        cart_items = Cart.objects.filter(id__in=request.session.get('cart_items', []))
        for cart in cart_items:
            Buy2.objects.create(
                user=order.user,
                product=cart.product,
                price=cart.product.price * cart.quantity,
                quantity=cart.quantity,
                address=order.user.address,
                order=order
            )

        # Clear the cart
        cart_items.delete()

        return redirect(pay3)

    else:
        payment_data = json.loads(request.POST.get("error[metadata]", "{}"))
        provider_order_id = payment_data.get("order_id", "")
        order = Order2.objects.get(provider_order_id=provider_order_id)
        order.status = PaymentStatus.FAILURE
        order.save()

        return redirect(pay3)



def cancel_order(req,id):
    data=Buy.objects.get(pk=id)
    data.delete()
    return redirect(shop_home)

def confirm_order(request, order_id):
    order = get_object_or_404(Buy, pk=order_id)

    # Check if the order is already confirmed to avoid unnecessary updates
    if not order.is_confirmed:
        order.is_confirmed = True
        order.save()

        # Send confirmation email
        subject = "Order Confirmation"
        message = f"Dear {order.user.first_name},\n\nYour order for {order.product} has been confirmed. Thank you for shopping with us!\n\nBest regards,\nYour Store Team"
        recipient_email = order.user.email  

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # This will be your email settings
            [recipient_email],
            fail_silently=False,
        )
    
    # After confirming the order, redirect to the order details or shop home page
    return redirect(shop_home)  # Replace with the actual URL name if it's different
