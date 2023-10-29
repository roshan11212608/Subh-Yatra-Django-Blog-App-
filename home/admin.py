from django.contrib import admin
from .models import *;
from django.contrib.auth.admin import UserAdmin


admin.site.register(Blog)
admin.site.register(CustomUser)
admin.site.register(Contact)
# Register your models here.
