from django.contrib import admin
from .models import User, UserVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password', 'phone', 'verified', 'date_joined', 'invite_code', 'activated_invite_code')
    search_fields = ('name', 'phone')



@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'phone', 'verification_code', 'attempts_remaining', 'verified', 'date_joined', 'date_when_verified')
