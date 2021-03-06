from django.contrib import admin
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('register/',views.registerPage, name='register'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),

    path('account/', views.accountSettings, name="account"),
    
    path('', views.home, name='home'),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customers, name="customer"),



    path('create-order/<str:pk>', views.createOrders, name="create_order"),
    path('update-order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete-order/<str:pk>', views.deleteOrder, name='delete_order') , 

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name= "reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name= "password_reset_complete"),


    #path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    ]