from django.urls import path, include
from accounts.views import UserSignupViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('signup', UserSignupViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
]