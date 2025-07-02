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
