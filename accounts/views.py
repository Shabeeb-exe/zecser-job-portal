from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, JobseekerProfile, EmployerProfile
from .serializers import UserSignupSerializer, UserLoginSerializer, JobseekerProfileSerializer, EmployerProfileSerializer, JobseekerProfileUpdateSerializer, EmployerProfileUpdateSerializer

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
            refresh_token = request.data.get("refersh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message" : "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class JobseekerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = JobseekerProfileSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
