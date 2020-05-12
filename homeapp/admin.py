from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import  UserAdminCreationForm,UserAdminChangeForm
from django.contrib.auth import get_user_model
from homeapp.models import SellerID,Sessionlog,Membership,Address,TryPeriod
from homeapp.activitytracker import Activity
admin.site.register(TryPeriod)
admin.site.register(Membership)
admin.site.register(Address)
admin.site.register(Activity)
admin.site.register(SellerID)


User= get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        ('User info', {'fields': ('email', 'firstname','lastname','dp','me','number','gender')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','active','slug','seller','buyer','staff','approve')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal=()
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Sessionlog)