from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import BrandUser, User


class BrandUserCreationForm(UserCreationForm):

    class Meta:
        model = BrandUser
        fields = ('username', 'email',  'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'type' field in the form
        self.fields.pop('type', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        self.instance.type = User.Type.BRAND
        # If a password is provided, set and encrypt it
        password = self.cleaned_data.get('new_password')
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user


class BrandUserChangeForm(UserChangeForm):
    password = forms.CharField(
        label="Password",
        strip=False,
        required=False,
        widget=forms.PasswordInput,
        help_text="Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using <a href=\"../password/\">this form</a>.",
    )

    class Meta:
        model = BrandUser
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)

        # If a password is provided, set and encrypt it
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user