from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render
from SimSimWeb.forms import *
from SimSimWeb.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    print 'come to home'
    print(request.user.username)
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


# def list_activity(require):
#     pass

    
def lock_activity(request):
    print("in lock activity right now")
    print(request.user)
    print(request.user.id)
    print(type(request.user))
    property_list = Properties.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id).distinct()
    locks = Locks.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id)
    property_activities = LockActivity.objects.filter(lock_id = locks).order_by('-lock_activity_time_stamp')
    context = {'property_list': property_list, 'property_activities': property_activities, 'selected_property': "All"}
    return render(request, 'SimSimWeb/lock_activity.html', context)

def display_activity(request):
    print("selecting property")
    property_list = Properties.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id).distinct()
    context = {'property_list': property_list}
    key = request.GET['select_property']
    print ("key"+key)
    if(key == 'All'):
        return lock_activity(request)
        # print("all selected")
        # locks = Locks.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id)
        # property_activities = LockActivity.objects.filter(lock_id = locks).order_by('-lock_activity_time_stamp')
        # activities = LockActivity.objects.filter(lock_id = locks).order_by('-lock_activity_time_stamp')
    else:
        print("a property is selected")
        selected_property = property_list.get(property_id = key)
        locks = Locks.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id, propertylocks__property_id = selected_property)
        property_activities = LockActivity.objects.filter(lock_id = locks).order_by('-lock_activity_time_stamp')
        # activities = LockActivity.objects.filter(lock_id = locks).order_by('-lock_activity_time_stamp')
    # paginator = Paginator(activities, 5)
    # page = request.GET.get('page')
    # try:
    #     property_activities = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     property_activities = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     property_activities = paginator.page(paginator.num_pages)
    context = {'property_list': property_list, 'property_activities': property_activities, 'selected_property': selected_property}
    print("rendering lock activity")
    return render(request, 'SimSimWeb/lock_activity.html', context)



def manage_properties(request):
    context = {}
    return render(request, 'SimSimWeb/manage_properties.html', context)
def profile(request):
    context = {}
    return render(request, 'SimSimWeb/profile.html', context)
