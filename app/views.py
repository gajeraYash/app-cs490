from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from app.forms import *
from app.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#push
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed')
    else:
        return render(request, 'app/index.html')

def test_page(request):
    return render(request, 'app/index.html')

def msgthread(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app:index'))
    else:
        thread_obj = Thread.objects.by_user(request.user)
        return render(request, 'app/message.html', {'thread_obj':thread_obj})

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'app/room.html'
    form_class = ComposeMSGForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

@login_required
def follow(request, username):
    follow_user = User.objects.get(username=username)
    if len(Follower.objects.filter(follower=request.user, following=follow_user)) > 0:
        instance = Follower.objects.get(follower=request.user, following=follow_user)
        instance.delete()
    else:
        Follower.objects.create(follower=request.user, following=follow_user)
    return HttpResponseRedirect('/user/'+username)

@login_required
def user_search(request):
    user_param = request.GET.get('user_search', None)
    if user_param:
        user_q = User.objects.filter(Q(username__icontains=user_param) | Q(
            first_name__icontains=user_param) | Q(last_name__icontains=user_param)).order_by('username')[:5]
        return render(request, 'app/partials/user_search.html', {'user_results': user_q})
        # return JsonResponse({'user_results':user_obj_q}, safe=False)
    else:
        print("No Value Provided")

@login_required
def msg_user(request):
    user_param = request.GET.get('msg_user', None)
    if user_param:
        user_q = User.objects.filter(Q(username__icontains=user_param) | Q(
            first_name__icontains=user_param) | Q(last_name__icontains=user_param)).order_by('username').exclude(username=request.user.username)[:5]
        print(user_q)
        return render(request, 'app/partials/msg_user.html', {'user_results': user_q})
        # return JsonResponse({'user_results':user_obj_q}, safe=False)
    else:
        print("No Value Provided")

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("app:index"))
    else:
        profile_data_obj = UserProfile.objects.get(user=request.user)
        return render(request, 'app/profile.html', {"profile_data": profile_data_obj})

def edit_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("app:login"))
    else:
        if request.method == 'POST':
            user_info_form = UserInfoDetailForm(request.POST, instance= request.user)
            user_profile_form = UserProfileDetailForm(request.POST, request.FILES, instance= request.user.userprofile)
            if (user_info_form.is_valid() and user_profile_form.is_valid()):
            
                user_info_form.save()
                user_profile_form.save()
                return HttpResponseRedirect(reverse("app:profile"))
            else:
                print("error while editing profile")
        else:
            user_info_form = UserInfoDetailForm(instance= request.user)
            user_profile_form = UserProfileDetailForm(instance= request.user.userprofile)
        return render(request, 'app/editprofile.html', {"profile_form": user_profile_form, "user_info": user_info_form})
        

def user_profile(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("app:index"))
    else:
        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
            profile_data_obj = UserProfile.objects.get(user=u)
            following = True if len(Follower.objects.filter(follower=request.user, following=u)) > 0 else False
            return render(request, 'app/profile.html', {"profile_data": profile_data_obj, "user_follow": following})
        else:
            print("checked NOP!")
            return render(request, 'app/profile.html', {"profile_data": False})


@login_required
def user_feed(request):
    feed_param = request.GET.get('feed_param', None)
    liked = list(Like.objects.filter(user= request.user).values_list('post',flat=True))
    if feed_param == 'FOLLOWING':
        following_list = (Follower.objects.filter(
            follower=request.user)).values_list('following', flat=True)
        user_feed_obj = UserAnnoucement.objects.all().select_related().prefetch_related('like_set').filter(
            Q(user=request.user) | Q(user__in=following_list)).order_by('-created')
        like_count = user_feed_obj.annotate(num_likes=Count('like'))
        return render(request, 'app/partials/user_feed.html', {'user_feed': user_feed_obj , 'like_count': like_count, 'liked':liked})
    elif feed_param:
        if User.objects.filter(username=feed_param).exists():
            user_q = User.objects.get(username=feed_param)
            user_feed_obj = UserAnnoucement.objects.filter(
                user=user_q).order_by('-created')
            like_count = user_feed_obj.annotate(num_likes=Count('like'))
            return render(request, 'app/partials/user_feed.html', {'user_feed': user_feed_obj, 'like_count': like_count, 'liked':liked })
        else:
            return render(request, 'app/partials/user_feed.html')
    else:
        user_feed_obj = UserAnnoucement.objects.filter(
            user=request.user).order_by('-created')
        like_count = user_feed_obj.annotate(num_likes=Count('like'))
        return render(request, 'app/partials/user_feed.html', {'user_feed': user_feed_obj, 'like_count': like_count, 'liked':liked})


def feed(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            announcement_form = UserTweet(request.POST, request.FILES)
            if announcement_form.is_valid():
                user = request.user
                announcement = announcement_form.save(commit=False)
                announcement.user = user
                announcement.save()
                return HttpResponseRedirect("/feed")
            else:
                print("error")
        else:
            announcement_form = UserTweet()
    return render(request, 'app/feed.html', {"announcement_form": announcement_form, })

            
@login_required
def user_post(request, post):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("app:index"))
    else:
        if UserAnnoucement.objects.get(id=post):
            post_obj = UserAnnoucement.objects.get(id=post)
            comment_obj = UserComment.objects.filter(post = post_obj)
            number_of_likes = post_obj.like_set.all().count()
            if request.method == "POST":
                comment_form = UserCommentForm(request.POST)
                if comment_form.is_valid():
                    user = request.user
                    comment = comment_form.save(commit=False)
                    comment.user = user
                    comment.post = post_obj
                    comment.save()
                    return HttpResponseRedirect(request.path_info)
                else:
                    print("error in posting comment")
            else:
                comment_form = UserCommentForm()
            return render(request,'app/post.html',{"post":post_obj,"comment":comment_obj,"comment_form":comment_form, 'likes_count':number_of_likes})
        else:
            print("checked NOP!")
            return render(request,'app/post.html',{"post":False})

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

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('app:password_change'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/change_password.html', {
        'form': form
    })

@login_required
@csrf_exempt
def like_ajax(request):
    if request.method == "POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            post_id = request.POST.get("post_id", None)
            if UserAnnoucement.objects.get(id=post_id):
                post_obj = UserAnnoucement.objects.get(id=post_id)
                user = request.user
                new_like, created = Like.objects.get_or_create(user=user, post=post_obj)
                if not created:
                    instance = Like.objects.get(user=user, post=post_obj)
                    instance.delete()
                    liked = False
                else:
                    liked = True
                ctx = {"post_id": post_id, "liked": liked}
                return JsonResponse(ctx)
            else:
                print("error")




def user_login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username'].lower()
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
