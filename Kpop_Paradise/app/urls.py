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

#------------------------------------------------------------------------------------------USER


    path('user_home',views.user_home),
    path('user_band/<int:id>/', views.concert_list, name='concert_list'),
    path('product/<int:id>/', views.view_pro, name='view_pro'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

 
    ]