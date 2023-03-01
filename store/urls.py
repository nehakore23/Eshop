from django.contrib import admin
from django.urls import path
from .views import store
from .views import home
from .views import cart
from . import views


urlpatterns = [
    path('', home),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('product/<str:pk>/', views.product, name="product"),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.Order, name='orders'),
    path('register/', views.registerpage, name="register"),
	path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]