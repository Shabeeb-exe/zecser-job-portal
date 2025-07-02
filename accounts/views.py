from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from accounts.models import User
from .serializers import UserSignupSerializer

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
