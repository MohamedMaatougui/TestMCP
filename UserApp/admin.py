from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','first_name')


admin.site.register(User,UserAdmin) 