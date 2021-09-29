from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from requests.auth import HTTPBasicAuth
import json
import requests
from .models import Customer, Products, Order
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, unauthenticated_user, allowed_users
from django.contrib.auth.models import Group

#from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
@unauthenticated_user
def registerPage(request):
        form = CreateUserForm()
        if request.method =="POST":
            form= CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username= form.cleaned_data.get('username')
                messages.success(request, 'Account Created for '+ username)
                return redirect('login')
        context={
            "form":form
        }
        return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
        if request.method == "POST":
            username= request.POST.get('username')
            password=request.POST.get('password')
            user= authenticate(request,username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')

            else: 
                messages.info(request, 'You entered invalid Credentials')
        return render(request, 'accounts/login.html')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers= Customer.objects.all()
    total_customers= customers.count()
    total_orders= orders.count()
    delivered= orders.filter(status='Delivered').count()
    pending= orders.filter(status='Pending').count()
    context ={
        "orders":orders,
        "customers":customers,
        "total_customers": total_customers,
        'total_orders':total_orders,
        'delivered': delivered,
        'pending':pending
    }
    return render(request, 'accounts/dashboard.html', context)
    
""" def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254724961618,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254724961618,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Henry",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success') """

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders= request.user.customer.order_set.all()
    total_orders= orders.count()
    delivered= orders.filter(status='Delivered').count()
    pending= orders.filter(status='Pending').count()

    context = {
        "orders":orders,
        "total_orders": total_orders,
        "delivered":delivered,
        "pending":pending
        }
    return render(request, 'accounts/user.html', context)

@login_required(login_url="login")


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
	    form = CustomerForm(request.POST, request.FILES,instance=customer)
	    if form.is_valid():
		    form.save()
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)



def products(request):
    products= Products.objects.all()
    return render(request, 'accounts/products.html', {'products':products})
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders= customer.order_set.all()
    customer_total_orders= orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context= {
        "customer":customer,
       "customer_total_orders": customer_total_orders,
       "orders":orders,
       "myFilter": myFilter,
    }
    return render(request, 'accounts/customers.html', context)

@login_required(login_url="login")
def createOrders(request, pk):
    OrderFormSet= inlineformset_factory(Customer,Order, fields=('product','status'))
    customer= Customer.objects.get(id=pk)
    formset= OrderFormSet(queryset=Order.objects.none(),  instance=customer)
    #form= OrderForm(initial={'customer':customer})
    if request.method =='POST':
        #form= OrderForm(request.POST)
        formset= OrderFormSet(request.POST,instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('home')

        #print(request.POST)
    context={
            "formset": formset
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url="login")
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    print(order)
    form= OrderForm(instance=order)
    if request.method== 'POST':
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={
        "form":form
    }
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url="login")
def deleteOrder(request, pk):
    order= Order.objects.get(id=pk)
    if request.method =='POST':
        order.delete()
        return redirect('home')
    context={
        'order':order
    }

    return render(request, 'accounts/delete.html', context)
    