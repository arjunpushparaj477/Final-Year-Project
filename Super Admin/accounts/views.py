from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserActivitySerializer, UserProfileSerializer
from .models import UserActivity
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'super_admin':
            return self.queryset
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        total_users = self.queryset.count()
        active_users = self.queryset.filter(status='active').count()
        return Response({
            'total_users': total_users,
            'active_users': active_users
        })

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def request_password_reset(request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{user.pk}/{token}/"
            
            send_mail(
                'Password Reset Request',
                f'Click here to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def reset_password(request, user_id, token):
        try:
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                user.set_password(request.data.get('password'))
                user.save()
                return Response({'message': 'Password reset successful'})
            return Response({'error': 'Invalid token'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    @api_view(['GET', 'PUT'])
    @permission_classes([IsAuthenticated])
    def user_profile(request):
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)