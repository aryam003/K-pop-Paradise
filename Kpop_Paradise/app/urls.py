from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),


    path('shop_home',views.shop_home),
    path('band/<int:id>/', views.shop_concert_list, name='concert_list'),
    

    path('user_home',views.user_home),
    # path('band/<id>', views.concert_list, name='concert_list'),
    # path('concert/<id>/book/', views.book_ticket, name='book_ticket'),
    path('band/<int:id>/', views.concert_list, name='concert_list'),
    # path('concerts/<int:id>/book/', views.book_ticket, name='book_ticket'),

 
    ]