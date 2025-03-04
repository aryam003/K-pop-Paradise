from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),

#------------------------------------------------------------------------------------------ADMIN

    path('shop_home',views.shop_home),
    path('shop_band/<int:id>/', views.shop_concert_list, name='concert_list'),
    path('about/',views.about),
#concert
    path('add-concert/', views.add_concert, name='add_concert'),
    path('edit_concert/<int:id>/', views.edit_concert, name='edit_concert'),
    path('delete_concert/<int:id>/', views.delete_concert, name='delete_concert'),
#product
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),
    # path('shop_view-bookings/', views.shop_view_bookings, name='view_bookings'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking-details/', views.ticket_booking_details, name='ticket_booking_details'), 
#------------------------------------------------------------------------------------------USER


    path('user_home',views.user_home),
    path('user_band/<int:id>/', views.concert_list, name='concert_list'),
    # path('shop_view_bookings/', views.user_view_bookings),
    path('concert/<int:concert_id>/book/', views.book_ticket, name='book_ticket'),
    # path('ticket-details/', views.ticket_view_bookings, name='ticket_details'),
    # path('my-tickets/', views.user_tickets, name='user_tickets'),
    path('user_tickets/', views.user_tickets, name='user_tickets'),

#---product
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),  # Delete cart item
    path('view-bookings/', views.view_bookings, name='view_bookings'),
    # path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('payment/callback/<int:booking_id>/', views.payment_callback, name='payment_callback'),

    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/',views. add_edit_profile, name='edit_profile'),
    path('checkout/', views.checkout_cart, name='checkout_cart'),

    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    # path('buy_pro/<id>',views.buy_pro,name='buy_pro'),







    path('buy_pro/<int:id>/', views.buy_pro, name='buy_pro'),
    path('book_ticket/<int:concert_id>/', views.book_ticket, name='book_ticket'),
    path('order_payment/', views.order_payment, name='order_payment'),
    path('pay/', views.pay, name='pay'),
    path('callback/', views.callback, name='callback'),



    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('buy_pro2/<int:id>/', views.buy_pro2, name='buy_pro2'),
    path('order_payment2/', views.order_payment2, name='order_payment2'),
    path('pay2/', views.pay2, name='pay2'),
    path('callback2/', views.callback2, name='callback2'),
    path('place_order/<id>/', views.place_order2, name='place_order2'),

    path('cart/address/', views.cart_address_page, name='cart_address_page'),
    
    # Route to the order payment page (step 2)
    path('order/payment3/', views.order_payment3, name='order_payment2'),
    
    # Route to handle the payment confirmation callback
    path('callback3/', views.callback3, name='callback2'),
    
    # Route to process the payment and finalize the order (final step after payment)
    path('pay3/', views.pay3, name='pay2'),
    
    path('cancel_order/<id>',views.cancel_order),
    path('confirm_order/<order_id>', views.confirm_order, name='confirm_order'),
     path('confirm_order/<int:order_id>/',views. confirm_order, name='confirm_order')

    


]
 
    