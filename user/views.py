from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login_page(request):
    return HttpResponse("Hello World. You are at the User Login view")


def register_page(request):
    return HttpResponse("Hello World. You are at the User Register view")


def user_page(request):
    return HttpResponse("Hello World. You are at the User view")
