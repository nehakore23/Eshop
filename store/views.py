from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
from.forms import CreateUserForm

@login_required(login_url='login')
def store(request):
    products = Product.get_all_products()
    print(products)
    return render(request, 'store.html', {'products': products})

@login_required(login_url='login')
def home(request):
    return render(request, 'Home.html')

@login_required(login_url='login')
def product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        # Get user account information
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity = request.POST['quantity']
        orderItem.save()

        return redirect('cart')

    context = {'product': product}
    return render(request, 'store.html', context)

@login_required(login_url='login')
def cart(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    context = {'order': order}
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def checkout(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    context = {'order': order}
    return render(request, 'checkout.html', context)


def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        return redirect('store')
    else:
        messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')