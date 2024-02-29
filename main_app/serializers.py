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
        fields = ['id', 'name', 'start_date', 'end_date']

class WeekSerializer(serializers.HyperlinkedModelSerializer):
    camp = serializers.PrimaryKeyRelatedField(queryset=Camp.objects.all())
    kids = serializers.PrimaryKeyRelatedField(many=True, queryset=Kid.objects.all())

    class Meta:
        model = Week
        fields = ['id', 'week_number', 'start_date', 'end_date', 'camp', 'kids']
        
class KidSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Kid
        fields = ['id', 'name', 'dob', 'school', 'allergies', 'emergency_contact', 'leaving_permissions', 'user']