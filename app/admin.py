from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserAnnoucements)
admin.site.register(Follower)