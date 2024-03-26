from django.urls import re_path

from authentication.social import views

urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        views.ProviderAuthView.as_view(),
        name="provider-auth",
    )
]
