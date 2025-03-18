from rest_framework import viewsets, permissions
from .models import Center
from .serializers import CenterSerializer

class CenterViewSet(viewsets.ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'super_admin':
            return self.queryset
        return self.queryset.filter(admin=self.request.user)