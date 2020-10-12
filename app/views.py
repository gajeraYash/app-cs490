
from django.http.response import HttpResponseRedirect
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from app.forms import *
from app.models import *
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed')
    else:
        return render(request, 'app/index.html')

def user_search(request):
    user_param = request.GET.get('user_search', None)
    if user_param:
        print("User params: "+user_param)
        user_q = User.objects.filter(Q(username__icontains=user_param) | Q(first_name__icontains=user_param) | Q(last_name__icontains=user_param)).order_by('username')
        user_obj_q = list(user_q.values('username','first_name','last_name'))
        print(user_obj_q)
        return render(request, 'app/partials/user_search.html', {'user_results':user_obj_q})
        # return JsonResponse({'user_results':user_obj_q}, safe=False)
    else:
        print("No Value Provided")
    
def user_feed(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            announcement_form = UserTweet(request.POST)
            if announcement_form.is_valid():
                user = request.user 
                announcement = announcement_form.save(commit=False)
                announcement.user = user
                announcement.save()
                return HttpResponseRedirect('/feed')
            else:
                print("error")
        else:
            announcement_form = UserTweet()

        profile_data = UserProfile.objects.get(user=request.user)
        usertweet_data = UserAnnoucements.objects.filter(user=request.user).order_by('-created')
        return render(request,'app/feed.html',{"profile_data":profile_data,"usertweet_data":usertweet_data,"announcement_form":announcement_form})

def user_signup_success(request):
    registered = True
    return render(request,'app/signup.html',{'registered': registered})

def user_signup(request):
    message = ''
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = UserProfileDOBForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('/signup/success')
        else:
            message = "Error: Submitting Request"
    else:
        user_form = SignUpForm()
        profile_form = UserProfileDOBForm()
    return render(request, 'app/signup.html', {'user_form': user_form,
                                                   'profile_form': profile_form,
                                                   'message': message})


def user_login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request,user)
            return HttpResponseRedirect("/feed")
        else:
            print("Error: Submitting Request")
    else:
        login_form = UserLoginForm()
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed')
    else:
        return render(request,"app/login.html", {'login_form':login_form})
    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
