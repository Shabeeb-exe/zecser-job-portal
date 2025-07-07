# urls.py
from django.urls import path, include
from .views import UserSignupViewSet, UserLoginView, JobseekerProfileViewSet, EmployerProfileViewSet
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', UserSignupViewSet.as_view({'post': 'create'})), 
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jobseeker-profile/', JobseekerProfileViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update'
    })),
    path('employer-profile/', EmployerProfileViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update'
    })),
]