from django.shortcuts import render


def home(request):
    print 'come to home'
    context = {}
    return render(request, "SimSimWeb/index.html", context)
