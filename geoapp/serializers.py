from rest_framework import serializers
from .models import UserProfile, UserDetails

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'image']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['f_name', 'email', 'phone', 'address']