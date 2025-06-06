from . import views
from django.urls import path

urlpatterns=[
    path('',views.home,name='home'),
    path('menu/',views.menu,name='menu'),
    path('contact/',views.contact,name='contact'),
    path('add_to_cart/<path:item_name>/',views.add_to_cart,name='add_to_cart'),
    # path('increment_to_cart/<str:item_name>/',views.increment_to_cart,name='increment_to_cart'),
    path('decrement_cart/<path:item_name>/',views.decrement_cart,name='decrement_cart'),
    path('remove_from_cart/<path:item_name>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('cart/',views.cart,name='cart'),
    path('upi/checkout/', views.upi_checkout, name='upi_checkout'),
    path('upi/confirm/<int:payment_id>/', views.mark_paid, name='mark_paid'),
    path('pay/', views.initiate_payment, name='pay'),
]