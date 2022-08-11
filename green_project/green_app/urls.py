from django.contrib import admin
from django.urls import path
from green_app import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
]