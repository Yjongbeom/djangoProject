from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import LoginSerializer

class UserViewSet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer

    def get_object(self):
        return self.request.user
