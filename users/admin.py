from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass