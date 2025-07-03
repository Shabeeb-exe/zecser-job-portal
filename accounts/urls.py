# urls.py
from django.urls import path, include
from accounts.views import UserSignupViewSet, JobseekerProfileViewSet, EmployerProfileViewSet

urlpatterns = [
    path('signup/', UserSignupViewSet.as_view({'post': 'create'})), 
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