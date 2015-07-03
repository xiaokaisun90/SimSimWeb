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
    print('!!!!!!!calling family function')
    property_list = Properties.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id).distinct()
    selected_property = None
    context = dict()
    if request.method == 'POST':
        formOne = selectPropertyForm(request.POST)
        # formTwo = familyMemberForm(request.POST)
        print('we got here')
        if formOne.is_valid():
            # print('input in form one')
            selected_property = formOne.cleaned_data['property']
            print(type(selected_property))
            context['selected_property'] = selected_property
            formTwo = familyMemberForm()
            print('formone complete')
            context['family_list'] = familyMemberHelper(selected_property)
            print(context['family_list'])
        # elif formTwo.is_valid():
        #     print('input in form two')
        #     mobile = formTwo.process_mobile()
        #     print mobile
        #     print("fuckoff")
        #     formOne = selectPropertyForm()
    else:
        print('no input')
        # print(list(property_list[:1])[0])
        formOne = selectPropertyForm()
        # formTwo = familyMemberForm()
        formTwo = False

    formOne.fields["property"].queryset = property_list
    context['selectPropertyForm'] = formOne
    context['familyMemberForm'] = formTwo
    

    return render(request, 'SimSimWeb/family.html', context)

def addMember(request):
    print('!!!!!!!calling addmember function')
    property_list = Properties.objects.filter(propertylocks__userpropertylocks__user_id = request.user.id).distinct()
    context = {}

    if request.method == 'POST':
        formTwo = familyMemberForm(request.POST)
        selected_property_pk = request.POST['current']
        selected_property = Properties.objects.get(pk = selected_property_pk)
        context['selected_property'] = selected_property
        print('this is before checking'+selected_property_pk)
        print('start checking ')
        if formTwo.is_valid():
            print('input in form two')
            mobile = formTwo.process_mobile()
            member = UserInfo.objects.get(primary_mobile_number = mobile)
            propertyLocks = PropertyLocks.objects.filter(property_id = selected_property)
            userRoleType = UserRoleTypes.objects.get(user_role_type__contains = 'family')
            for lock in propertyLocks:
                userPropertyLock = UserPropertyLocks(user_id = member, property_lock_id = lock, user_role_type_id = userRoleType)
                userPropertyLock.save()
            print (selected_property)
            print (type(selected_property))
            print mobile

            userRole = UserRoleTypes.objects.get(user_role_type__contains = 'family')
            member = UserInfo.objects.get(primary_mobile_number = mobile).user_id

            print("fuckoff")
    else:
        print('no input')
        # print(list(property_list[:1])[0])
        # formTwo = familyMemberForm()
        formTwo = familyMemberForm()
    context['family_list'] = familyMemberHelper(selected_property)
    formOne = selectPropertyForm()
    formOne.fields["property"].queryset = property_list
    context['selectPropertyForm'] = formOne
    context['familyMemberForm'] = formTwo
    return render(request, 'SimSimWeb/family.html', context)
# def list_activity(require):
#     pass

def familyMemberHelper(property_id):
    familyList = []
    propertyLocks = PropertyLocks.objects.filter(property_id = property_id)
    familyLocks = UserPropertyLocks.objects.filter(property_lock_id = propertyLocks, user_role_type_id__user_role_type__contains = 'family')
    for lock in familyLocks:
        if lock.user_id not in familyList:
            familyList.append(lock.user_id)
    return familyList

def deleteMember(request):
    context={}
    if request.method == 'POST':
        mobile = request.POST['member']
        member = UserInfo.objects.get(primary_mobile_number = mobile)
        print(member)
        print(type(member))
        property_id = request.POST['current']
        selected_property = Properties.objects.get(pk = property_id)
    propertyLocks = PropertyLocks.objects.filter(property_id = selected_property)
    familyLocks = UserPropertyLocks.objects.filter(property_lock_id = propertyLocks, user_id = member)
    print(len(familyLocks))
    for lock in familyLocks:
        lock.delete()
    familyLocks = UserPropertyLocks.objects.filter(property_lock_id = propertyLocks, user_id = member)
    print(len(familyLocks))
    context['selected_property'] = selected_property
    context['selectPropertyForm'] = selectPropertyForm()
    context['familyMemberForm'] = familyMemberForm()
    context['family_list'] = familyMemberHelper(selected_property)
    return render(request, 'SimSimWeb/family.html', context)

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
