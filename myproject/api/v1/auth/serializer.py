from rest_framework.serializers import ModelSerializer
from blogApp.models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        fields=('id','username','email','password','first_name')
        model =User

class UserProfileSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        fields=("user","profile_picture","bio","information")
        model=UserProfile