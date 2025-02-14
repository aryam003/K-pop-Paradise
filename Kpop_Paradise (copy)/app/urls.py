from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),

#------------------------------------------------------------------------------------------ADMIN

    path('shop_home',views.shop_home),
    path('shop_band/<int:id>/', views.shop_concert_list, name='concert_list'),
#concert
    path('add-concert/', views.add_concert, name='add_concert'),
    path('edit_concert/<int:id>/', views.edit_concert, name='edit_concert'),
    path('delete_concert/<int:id>/', views.delete_concert, name='delete_concert'),
#product
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),
    # path('shop_view-bookings/', views.shop_view_bookings, name='view_bookings'),
    
#------------------------------------------------------------------------------------------USER


    path('user_home',views.user_home),
    path('user_band/<int:id>/', views.concert_list, name='concert_list'),
    # path('shop_view_bookings/', views.user_view_bookings),
    path('concert/<int:concert_id>/book/', views.book_ticket, name='book_ticket'),
    # path('ticket-details/', views.ticket_view_bookings, name='ticket_details'),



#---product
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),  # Delete cart item
    path('view-bookings/', views.view_bookings, name='view_bookings'),
    # path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    # path('ticket_view-bookings/', views.ticket_view_bookings, name='ticket_view_bookings'),

  
 
    ]