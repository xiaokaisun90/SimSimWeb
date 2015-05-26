from django.contrib.auth import authenticate, login
from django.shortcuts import render
from SimSimWeb.forms import RegistrationForm
from SimSimWeb.models import *


def home(request):
    print 'come to home'
    context = {}
    return render(request, "SimSimWeb/index.html", context)

def register(request):
    print 'first line of register'
    context = {}
    print request
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        print 'come into GET'
        context['form'] = RegistrationForm()
        return render(request, 'SimSimWeb/register.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        print 'form is not valid'
        context['form'] = form
        return render(request, 'SimSimWeb/register.html', context)
    else:
        new_user = User(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                        primary_mobile_number=form.cleaned_data['phone_number'])
        new_user.save()
        print "username", new_user.username

    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'],
                            )

    login(request,new_user)
    return render(request, "SimSimWeb/index.html",{})

def dashboard(request):
    context = {}
    return render(request, 'SimSimWeb/guest_request.html', context)

def guest_list(request):
    print 'in guest_list'
    context = {}
    return render(request, 'SimSimWeb/guest_list.html', context)

def family(request):
    context = {}
    return render(request, 'SimSimWeb/family.html', context)

def lock_activity(request):
    context = {}
    return render(request, 'SimSimWeb/lock_activity.html', context)
def manage_properties(request):
    context = {}
    return render(request, 'SimSimWeb/manage_properties.html', context)
def profile(request):
    context = {}
    return render(request, 'SimSimWeb/profile.html', context)
