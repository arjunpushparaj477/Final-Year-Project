from rest_framework import serializers
from .models import User, UserActivity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'status', 'phone_number', 'address', 'two_factor_enabled', 
                 'last_login', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'