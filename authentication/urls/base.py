from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter

from authentication import views
from authentication import view_influencer

router = DefaultRouter()
router.register("users", views.UserViewSet)
router.register("influencers", view_influencer.InfluencerViewSet)

User = get_user_model()

urlpatterns = router.urls
