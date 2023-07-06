"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('createblog',views.createblog),
    path('saveblog',views.saveblog),
    path('viewfull/<int:id>',views.viewfullblog),
    path('login',views.login),
    path('register',views.register),
    path('registeruser',views.registeruser),
    path('loginvalidate',views.loginvalidate),
    path('logout',views.logout),
    path('myblogs',views.myblogs),
    path('edit/<int:id>',views.edit),
    path('editvalidate',views.editvalidate),
    path('delete/<int:id>',views.delete),
    path('viewfull_personal/<int:id>',views.viewpersonal),
    path('create-checkout-session',views.create_checkout_session),
    path('success',views.success),
    path('fail',views.fail),
    path('premium',views.premium),
    path('webhooks',views.webhook)

]
