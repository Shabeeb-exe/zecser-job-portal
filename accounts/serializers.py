from rest_framework import serializers
from .models import User, JobseekerProfile, EmployerProfile, RoleEnum
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
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)

        if user.role == RoleEnum.JOBSEEKER.value:
            JobseekerProfile.objects.create(user=user)
        elif user.role == RoleEnum.EMPLOYER.value:
            EmployerProfile.objects.create(user=user)
        
        return user
    
class JobseekerProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = JobseekerProfile
        fields = [
            'id', 'email', 'full_name', 'resume', 'skills', 'education', 
            'experience', 'portfolio_url', 'github_url', 'desired_salary',
            'location', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class EmployerProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = EmployerProfile
        fields = [
            'id', 'email', 'full_name', 'company_name', 'company_logo',
            'company_website', 'company_size', 'industry', 'founded_year',
            'location', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

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