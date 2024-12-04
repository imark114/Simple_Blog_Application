from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Blog

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']
        password2 = validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})

        user = get_user_model()
        
        if user.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "This email already exists"})
        
        new_user = user.objects.create(username = username, email = email, first_name = first_name, last_name= last_name)
        new_user.set_password(password)
        new_user.save()
        return new_user

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture', 'facebook', 'instagram', 'linkedin', 'twitter']


class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

class BlogSerializer(serializers.ModelSerializer):
    author = SimpleAuthorSerializer(read_only = True)
    class Meta:
        model = Blog
        fields = '__all__'