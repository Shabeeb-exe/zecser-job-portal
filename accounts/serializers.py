from rest_framework import serializers
from .models import User, JobseekerProfile, EmployerProfile, RoleEnum, Job
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

    def validate(self, attrs):
        if self.context['request'].user.role != RoleEnum.JOBSEEKER.value:
            raise serializers.ValidationError("Only jobseekers can update this profile")
        return attrs

    def create(self, validated_data):
        # Add the current user to the profile data
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class EmployerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = [
            'company_name', 'company_logo', 'company_website',
            'company_size', 'industry', 'founded_year', 'location'
        ]
        extra_kwargs = {
            'company_logo': {'required': False},
            'user': {'read_only': True}
        }

    def validate(self, attrs):
        if self.context['request'].user.role != RoleEnum.EMPLOYER.value:
            raise serializers.ValidationError("Only employers can update this profile")
        return attrs
    
    def create(self, validated_data):
        # Add the current user to the profile data
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='employer.company_name', read_only=True)
    company_logo = serializers.SerializerMethodField()
    salary_min = serializers.SerializerMethodField()
    salary_max = serializers.SerializerMethodField()

    
    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'company_name', 'company_logo', 'title', 
            'description', 'requirements', 'location', 'job_type', 
            'salary', 'application_deadline', 'is_active', 'created_at',
            'updated_at','salary_min', 'salary_max'
        ]
        read_only_fields = ['id', 'employer', 'created_at', 'updated_at']

    def get_salary_min(self, obj):
        min_val, _ = self._parse_salary(obj.salary)
        return min_val

    def get_salary_max(self, obj):
        _, max_val = self._parse_salary(obj.salary)
        return max_val

    def _parse_salary(self, salary_str):
        """Shared helper method for parsing salaries"""
        if not salary_str:
            return None, None

        try:
            # Remove $ and commas, then split on hyphen
            clean_str = salary_str.replace('$', '').replace(',', '')
            parts = clean_str.split('-')
            
            if len(parts) == 1:
                # Single value ("50000")
                salary = int(parts[0])
                return salary, salary
            elif len(parts) == 2:
                # Range ("80000-100000")
                return int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            pass
        
        return None, None    
                
    def get_company_logo(self, obj):
        if obj.employer.company_logo:
            return self.context['request'].build_absolute_uri(obj.employer.company_logo.url)
        return None

class JobUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements', 'location', 
            'job_type', 'salary', 'application_deadline', 'is_active'
        ]