from rest_framework import serializers
from .models import User, JobseekerProfile, EmployerProfile, RoleEnum
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        # Hashing the password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include  "email" and "password". '
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs

class JobseekerProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = JobseekerProfile
        fields = [
            'id', 'email', 'full_name', 'resume', 'skills', 'education', 
            'experience', 'portfolio_url', 'github_url', 'desired_salary',
            'location', 'is_available'
        ]
        read_only_fields = ['id']

class EmployerProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = EmployerProfile
        fields = [
            'id', 'email', 'full_name', 'company_name', 'company_logo',
            'company_website', 'company_size', 'industry', 'founded_year',
            'location'
        ]
        read_only_fields = ['id']

class JobseekerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobseekerProfile
        fields = [
            'resume', 'skills', 'education', 'experience',
            'portfolio_url', 'github_url', 'desired_salary',
            'location', 'is_available'
        ]
        extra_kwargs = {
            'resume': {'required': False},
        }

class EmployerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = [
            'company_name', 'company_logo', 'company_website',
            'company_size', 'industry', 'founded_year', 'location'
        ]
        extra_kwargs = {
            'company_logo': {'required': False},
        }