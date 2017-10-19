from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'login/index.html')

def process(request):
    print request.POST
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        user = User.objects.add_user(request.POST)
        request.session['id'] = user.id
        messages.success(request, "You have successfully registered")
        return redirect('/success')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/success')
    else:
        messages.error(request, login_return['error'])
        return redirect('/')

def success(request):
    context = {
        "user": User.objects.get(id=request.session['id']),
        "all_users" : User.objects.all()
    }
    return render(request, 'login/success.html', context)

def reset(request):
    User.objects.all().delete()
    return redirect('/')
