from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Camp, Week, Kid

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'is_staff', 'id']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CampSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Camp
        fields = '__all__'

class WeekSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Week
        fields = '__all__'
        
class KidSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kid
        fields = '__all__'