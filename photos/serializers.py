from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Photo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
