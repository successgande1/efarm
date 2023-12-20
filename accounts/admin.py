from django.contrib import admin
from .models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'role', 'image')
    list_per_page = 6


admin.site.register(Profile, ProfileAdmin)