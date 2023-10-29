
from django.contrib import admin
from django.urls import path
from home.views import *;

urlpatterns = [
    path("",indexpage),
    path("login",loginUser),
    path("register",registerUser),
    path("logout",logoutUser),
    path('add',add),
    path('delete/<int:blog_id>',delete),
    path('update/<int:blog_id>',update),
    path('update/profile',updateprofile),
    path('forgotpassword',forgotpassword),
    path('contact',contact)

]
