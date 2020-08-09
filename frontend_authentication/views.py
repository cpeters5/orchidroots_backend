from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth

def index(request):
    return render(request, 'frontend_authentication/index.html')

def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect(redirect_to='/')
    response.set_cookie('is_loggedin', 'false')
    return response