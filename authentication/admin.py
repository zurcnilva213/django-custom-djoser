from django.contrib import admin

from authentication.forms import BrandUserCreationForm, BrandUserChangeForm
from authentication.models import User, Influencer, BrandUser


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'email',  'username', "last_login", "date_joined"]


admin.site.register(User, UserAdmin)


@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email')


@admin.register(BrandUser)
class BrandUserAdmin(admin.ModelAdmin):
    add_form = BrandUserCreationForm
    form = BrandUserCreationForm
    list_display = ('pk', 'first_name', 'last_name', 'email')
