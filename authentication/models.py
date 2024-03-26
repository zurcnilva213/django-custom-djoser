from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Type(models.TextChoices):
        INFLUENCER = "INFLUENCER", "INFLUENCER"
        BRAND = "BRAND", "BRAND"
        COMPANY = "COMPANY", "COMPANY"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=400, null=True, blank=True)
    last_name = models.CharField(max_length=400, null=True, blank=True)
    password = models.CharField(max_length=400)
    username = models.CharField(max_length=150, unique=True, blank=True)
    type = models.CharField(max_length=15, choices=Type.choices, null=True, blank=True)

    class Meta:
        db_table = 'users'


class Influencer(User):

    class Meta:
        verbose_name = 'Influencer'
        verbose_name_plural = 'Influencers'

    birthday = models.DateField(_("Birthday"), null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    instagram_handle = models.CharField(max_length=250, null=True, blank=True)
    tiktok_handle = models.CharField(max_length=250, null=True, blank=True)
    facebook_handle = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BrandUser(User):

    class Meta:
        verbose_name = 'BrandUser'
        verbose_name_plural = 'BrandUsers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
