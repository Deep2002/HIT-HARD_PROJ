from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('contact', views.sendMeassage, name='contact'),
    path('cart', views.cart, name='cart'),
    path('delete_item', views.delete_item, name='delete_item'),
    path('order_submit', views.order_submit, name='order_submit'),
]
