from django.apps import apps
from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

DJOSER_SETTINGS_NAMESPACE = "authentication"

auth_module, user_model = django_settings.AUTH_USER_MODEL.rsplit(".", 1)

User = apps.get_model(auth_module, user_model)


class ObjDict(dict):
    def __getattribute__(self, item):
        try:
            val = self[item]
            if isinstance(val, str):
                val = import_string(val)
            elif isinstance(val, (list, tuple)):
                val = [import_string(v) if isinstance(v, str) else v for v in val]
            self[item] = val
        except KeyError:
            val = super(ObjDict, self).__getattribute__(item)

        return val


default_settings = {
    "STRIPE_ENDPOINT_SECRET": "whsec_pvuv6oonqW2IZk5QzlYPMUn5EEeseM39",
    "USER_ID_FIELD": User._meta.pk.name,
    "LOGIN_FIELD": User.EMAIL_FIELD,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "reset-password/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": False,
    "USER_CREATE_PASSWORD_RETYPE": False,
    "SET_PASSWORD_RETYPE": False,
    "PASSWORD_RESET_CONFIRM_RETYPE": False,
    "SET_USERNAME_RETYPE": False,
    "USERNAME_RESET_CONFIRM_RETYPE": False,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": False,
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",
    "SERIALIZERS": ObjDict(
        {
            "activation": "authentication.serializers.ActivationSerializer",
            "password_reset": "authentication.serializers.SendEmailResetSerializer",
            "password_reset_confirm": "authentication.serializers.PasswordResetConfirmSerializer",
            "password_reset_confirm_retype": "authentication.serializers.PasswordResetConfirmRetypeSerializer",
            "set_password": "authentication.serializers.SetPasswordSerializer",
            "set_password_retype": "authentication.serializers.SetPasswordRetypeSerializer",
            "set_username": "authentication.serializers.SetUsernameSerializer",
            "set_username_retype": "authentication.serializers.SetUsernameRetypeSerializer",
            "username_reset": "authentication.serializers.SendEmailResetSerializer",
            "username_reset_confirm": "authentication.serializers.UsernameResetConfirmSerializer",
            "username_reset_confirm_retype": "authentication.serializers.UsernameResetConfirmRetypeSerializer",
            "user_create": "authentication.serializers.UserCreateSerializer",
            "user_create_password_retype": "authentication.serializers.UserCreatePasswordRetypeSerializer",
            "user_delete": "authentication.serializers.UserDeleteSerializer",
            "user": "authentication.serializers.UserSerializer",
            "current_user": "authentication.serializers.UserSerializer",
            "token": "authentication.serializers.TokenSerializer",
            "token_create": "authentication.serializers.TokenCreateSerializer",
        }
    ),
    "EMAIL": ObjDict(
        {
            "activation": "authentication.email.ActivationEmail",
            "confirmation": "authentication.email.ConfirmationEmail",
            "password_reset": "authentication.email.PasswordResetEmail",
            "password_changed_confirmation": "authentication.email.PasswordChangedConfirmationEmail",
            "username_changed_confirmation": "authentication.email.UsernameChangedConfirmationEmail",
            "username_reset": "authentication.email.UsernameResetEmail",
        }
    ),
    "CONSTANTS": ObjDict({"messages": "authentication.constants.Messages"}),
    "LOGOUT_ON_PASSWORD_CHANGE": False,
    "CREATE_SESSION_ON_LOGIN": False,
    "SOCIAL_AUTH_TOKEN_STRATEGY": "authentication.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": ['http://localhost:8000/facebook', 'http://localhost:8000/google'],
    "HIDE_USERS": True,
    "PERMISSIONS": ObjDict(
        {
            "activation": ["rest_framework.permissions.AllowAny"],
            "password_reset": ["rest_framework.permissions.AllowAny"],
            "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_password": ["authentication.permissions.CurrentUserOrAdmin"],
            "username_reset": ["rest_framework.permissions.AllowAny"],
            "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_username": ["authentication.permissions.AdminOnly"],
            "user_create": ["rest_framework.permissions.AllowAny"],
            "user_delete": ["authentication.permissions.AdminOnly"],
            "user": ["authentication.permissions.CurrentUserOrAdmin"],
            "user_list": ["authentication.permissions.AdminOnly"],
            "token_create": ["rest_framework.permissions.AllowAny"],
            "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
        }
    ),
}

SETTINGS_TO_IMPORT = ["TOKEN_MODEL", "SOCIAL_AUTH_TOKEN_STRATEGY"]


class Settings:
    def __init__(self, default_settings, explicit_overriden_settings: dict = None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        overriden_settings = (
            getattr(django_settings, DJOSER_SETTINGS_NAMESPACE, {})
            or explicit_overriden_settings
        )

        self._load_default_settings()
        self._override_settings(overriden_settings)
        self._init_settings_to_import()

    def _load_default_settings(self):
        for setting_name, setting_value in default_settings.items():
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)

    def _override_settings(self, overriden_settings: dict):
        for setting_name, setting_value in overriden_settings.items():
            value = setting_value
            if isinstance(setting_value, dict):
                value = getattr(self, setting_name, {})
                value.update(ObjDict(setting_value))
            setattr(self, setting_name, value)

    def _init_settings_to_import(self):
        for setting_name in SETTINGS_TO_IMPORT:
            value = getattr(self, setting_name)
            if isinstance(value, str):
                setattr(self, setting_name, import_string(value))


class LazySettings(LazyObject):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = Settings(default_settings, explicit_overriden_settings)


settings = LazySettings()


def reload_djoser_settings(*args, **kwargs):
    global settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == DJOSER_SETTINGS_NAMESPACE:
        settings._setup(explicit_overriden_settings=value)


setting_changed.connect(reload_djoser_settings)
