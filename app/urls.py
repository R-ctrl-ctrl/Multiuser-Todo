from unicodedata import name
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='home'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('main',views.main,name='main'),
    path('logout',views.userlogout,name='logout'),
    path('addtodo',views.addtodo,name='addtodo'),
    path('deletetodo/<int:id>/',views.deleteTodo,name='deletetodo'),
    path('updatetodo/<int:id>/',views.updateTodo,name='updatetodo')
]