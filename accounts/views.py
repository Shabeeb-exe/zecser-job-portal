from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Job, User, JobseekerProfile, EmployerProfile, RoleEnum
from .serializers import UserSignupSerializer, UserLoginSerializer, JobseekerProfileSerializer, EmployerProfileSerializer, JobseekerProfileUpdateSerializer, EmployerProfileUpdateSerializer, JobSerializer, JobUpdateSerializer
from .permissions import IsJobseeker, IsEmployer
from rest_framework import filters
from django_filters import rest_framework as djangofilters
from django.db.models import IntegerField, Case, When, Value
from django.db.models.functions import Cast, Substr, StrIndex

# Create your views here.
class UserSignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    http_method_names = ['post']  # Only allow POST for signup
    permission_classes = [permissions.AllowAny]
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
            }
        }, status=status.HTTP_200_OK)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message" : "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class JobseekerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = JobseekerProfileSerializer
    permission_classes = [IsAuthenticated, IsJobseeker]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        return JobseekerProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        # Correct way to get first item from queryset
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.first()
        if obj is None:
            # Create empty profile if none exists
            obj = JobseekerProfile.objects.create(
                user=self.request.user,
                skills='',
                education='',
                experience=''
            )
        return obj
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobseekerProfileUpdateSerializer
        return JobseekerProfileSerializer
    
    def create(self, request, *args, **kwargs):
        if hasattr(request.user, 'jobseeker_profile'):
            return Response(
                {'error' : 'Jobseeker profile already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'Job seeker profile created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message' : 'Jobseeker profile deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    
class EmployerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        return EmployerProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        # Correct way to get first item from queryset
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.first()
        if obj is None:
            # Create empty profile if none exists
            obj = EmployerProfile.objects.create(
                user=self.request.user,
                company_name='',
                company_website=''
            )
        return obj
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmployerProfileUpdateSerializer
        return EmployerProfileSerializer
    
    def create(self, request, *args, **kwargs):
        if hasattr(request.user, 'employer_profile'):
            return Response(
                {'error' : 'Employer profile already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'Employer profile created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Handle PUT requests (full update)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests (partial update)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message' : 'Employer profile deleted successfully'},status=status.HTTP_204_NO_CONTENT)

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_backends = [djangofilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'job_type' : ['exact','in'],
        'location' : ['exact','icontains'],
        'is_active' : ['exact'],
        'created_at':['gte','lte','exact']
    }
    search_fields = ['title', 'description', 'requirements', 'employer__company_name']
    ordering_fields = ['created_at', 'salary', 'title']
    ordering = ['-created_at']  # Default ordering

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsEmployer()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Job.objects.all()
        
        # For authenticated employers, show their own jobs
        if self.request.user.is_authenticated and self.request.user.role == RoleEnum.EMPLOYER.value:
            queryset = queryset.filter(employer__user=self.request.user)
        else:
            # For everyone else (including unauthenticated), show only active jobs
            queryset = queryset.filter(is_active=True)
        
        # Salary filtering
        min_salary = self.request.query_params.get('min_salary')
        max_salary = self.request.query_params.get('max_salary')
        
        if min_salary or max_salary:
            try:
                min_salary_val = int(min_salary) if min_salary else 0
                max_salary_val = int(max_salary) if max_salary else float('inf')
                
                # Get all jobs and filter in Python (less efficient but more reliable)
                filtered_jobs = []
                for job in queryset:
                    salary_min, salary_max = self._parse_salary(job.salary)
                    if salary_min is not None and salary_max is not None:
                        if (not min_salary or salary_max >= min_salary_val) and \
                        (not max_salary or salary_min <= max_salary_val):
                            filtered_jobs.append(job.id)
                
                # Return filtered queryset
                return queryset.filter(id__in=filtered_jobs)
                
            except ValueError:
                # Handle invalid salary values
                pass
                
        return queryset

    def _parse_salary(self, salary_str):
        """Helper method to parse salary string into min/max values"""
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

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobUpdateSerializer
        return JobSerializer
    
    def perform_create(self, serializer):
        # Automatically set the employer to the current user's employer profile
        employer_profile = self.request.user.employer_profile
        serializer.save(employer=employer_profile)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Verify that the employer owns this job
        if request.user.role == RoleEnum.EMPLOYER.value and instance.employer.user != request.user:
            return Response(
                {'error': 'You can only update your own jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Verify that the employer owns this job
        if request.user.role == RoleEnum.EMPLOYER.value and instance.employer.user != request.user:
            return Response(
                {'error': 'You can only delete your own jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(
            {'message': 'Job deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )