from authentication.models import Influencer, User
from authentication.serializers import InfluencerSerializer
from authentication.views import UserViewSet


class InfluencerViewSet(UserViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def perform_create(self, serializer):
        influencer = Influencer(
            username=serializer.data.get('username'),
            email=serializer.data.get('email'),
            mobile=serializer.data.get('mobile'),
            first_name=serializer.data.get('first_name'),
            last_name=serializer.data.get('last_name'),
            birthday=serializer.data.get('birthday'),
            instagram_handle=serializer.data.get('instagram_handle'),
            tiktok_handle=serializer.data.get('tiktok_handle'),
            facebook_handle=serializer.data.get('facebook_handle'),
            type=User.Type.INFLUENCER,
        )
        influencer.set_password(serializer.data["password"])
        influencer.save()
