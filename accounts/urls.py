# urls.py
from django.urls import path, include
from .views import ResendVerificationEmail, UserSignupViewSet, UserLoginView, UserLogoutView, JobseekerProfileViewSet, EmployerProfileViewSet, JobViewSet, VerifyEmailView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', UserSignupViewSet.as_view({'post': 'create'})), 
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationEmail.as_view(), name='resend-verification'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jobseeker-profile/', JobseekerProfileViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('employer-profile/', EmployerProfileViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    # job creation and listing
    path('jobs/', JobViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='job-list'),
    # job updation and deletion
    path('jobs/<int:pk>/', JobViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='job-detail'),
]