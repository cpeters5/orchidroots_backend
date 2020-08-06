from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.models import Group
# from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    list_filter = ('is_superuser', 'email_verified',)
    list_display = ('fullname', 'username', 'email',
                    'email_verified', 'verify_mail_code', 'reset_pass_code')
    fieldsets = (
        (
            'Personal Information',
            {
                'fields':
                    (
                        'fullname', 'email', 'username', 'photo', 'verify_mail_code', 'is_superuser', 'is_staff', 'email_verified',
                    )
            }
        ),
        (
            'Important dates',
            {
                'fields':
                    (
                        'last_login', 'date_joined',
                    )
            }
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email')}
         ),
    )


class PhotographerAdmin(admin.ModelAdmin):
    pass
    list_display = ('author_id', 'fullname', 'user_id',
                    'displayname', 'expertise')
    list_filter = ('expertise',)
    fields = ['author_id', ('fullname', 'displayname'),
              ('affiliation', 'status'), 'url']
    ordering = ['fullname']
    search_fields = ['author_id', 'fullname']


admin.site.register(User, MyUserAdmin)
admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(Tier)
admin.site.register(Photographer, PhotographerAdmin)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
