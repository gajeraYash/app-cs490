from django.urls import path
from . import views


app_name = 'app'  # here for namespacing of urls.

urlpatterns = [
    path('', views.index, name="index"),
    path('test', views.test_page, name="testpage"),

    # sign up
    path('signup', views.user_signup, name="signup"),
    path('signup/success', views.user_signup_success, name="signup-success"),

    # login logout
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),

    # feed
    path('feed', views.feed, name="feed"),
    path('post/<int:post>', views.user_post, name="user_post"),

    # getfeed
    path('user/search', views.user_search, name="user_search"),
    path('user/feed', views.user_feed, name="user_feed"),

    # profile
    path('profile', views.profile, name="profile"),
    path('profile/edit', views.edit_profile, name="profile_edit"),
    path('user/<str:username>', views.user_profile, name="user_profile"),

    # messages
    path('message', views.msgthread, name="message"),
    path('message/search', views.msg_user, name="msguser"),
    path('message/<str:username>/', views.ThreadView.as_view(), name='chat_room'),

    #follow
    path('follow/<str:username>/', views.follow, name='follow'),

    #like
    path('post/like', views.like_ajax, name='like_ajax'),

    #password change
    path('password', views.change_password, name='password_change'),
]
