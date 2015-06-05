from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render
from SimSimWeb.forms import *
from SimSimWeb.models import *
from django.contrib.auth.decorators import login_required


def home(request):
    print 'come to home'
    context = {}
    return render(request, "SimSimWeb/index.html", context)

@transaction.atomic
def register(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        print 'come into GET'
        context['form'] = RegistrationForm()
        return render(request, 'SimSimWeb/register.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    # print form
    if not form.is_valid():
        print 'form is not valid'
        context['form'] = form
        return render(request, 'SimSimWeb/register.html', context)
    else:
        new_user = User(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                        )
        new_user.set_password(new_user.password)
        new_user.save()
        new_user_info = UserInfo(user_id=new_user, primary_mobile_number=form.cleaned_data['primary_mobile_number'])
        print 'xx', new_user_info.user_id
        
        print new_user.password
        print "username", new_user.username

    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'],
                            )
    login(request, new_user)
    return render(request, "SimSimWeb/index.html", {})

@transaction.atomic
def dashboard(request):
    context = {}
    if request.method == 'GET':
        print 'come into GET'
        context['form'] = GuestAccessRequestForm()
        print context
        return render(request, 'SimSimWeb/guest_request.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        print 'form is not valid'
        context['form'] = form
        return render(request, 'SimSimWeb/guest_request.html', context)
    else:
        new_guest_request = GuestAccessRequestQueue(property_id=request.POST['property_id'],

        )

    return render(request, 'SimSimWeb/guest_request.html', context)
def introduction(request):
    context = {}
    return render(request, 'SimSimWeb/how_it_works.html', context)


def guest_list(request):
    print 'in guest_list'
    context = {}
    return render(request, 'SimSimWeb/guest_list.html', context)

def family(request):
    context = {}
    return render(request, 'SimSimWeb/family.html', context)

def lock_activity(request):
    print("in lock activity right now")
    print(request.user)
    print(request.user.id)
    print(type(request.user))
    property_list = Properties.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id).distinct()
    print(len(property_list))
    try:
        selected_property = Properties.objects.get(pk = request.POST['current_property'])
        print("got the properties")
    except (KeyError, Properties.DoesNotExist):
        property_activities = LockActivity.objects.all()
        print("no property selected")
    else:
        property_activities = LockActivity.objects.all()
    context = {'property_list': property_list, 'property_activities': property_activities}
    return render(request, 'SimSimWeb/lock_activity.html', context)


def manage_properties(request):
    context = {}
    return render(request, 'SimSimWeb/manage_properties.html', context)
def profile(request):
    context = {}
    return render(request, 'SimSimWeb/profile.html', context)
