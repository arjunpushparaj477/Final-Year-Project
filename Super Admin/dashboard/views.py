from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enhanced_analytics(request):
    now = timezone.now()
    last_month = now - timedelta(days=30)
    last_week = now - timedelta(days=7)

    return Response({
        'user_metrics': {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'new_users': {
                'weekly': User.objects.filter(date_joined__gte=last_week).count(),
                'monthly': User.objects.filter(date_joined__gte=last_month).count(),
            },
            'by_role': User.objects.values('role').annotate(count=Count('id')),
            'by_status': User.objects.values('status').annotate(count=Count('id')),
        },
        'center_metrics': {
            'total_centers': Center.objects.count(),
            'active_centers': Center.objects.filter(status='active').count(),
            'new_centers': {
                'weekly': Center.objects.filter(created_at__gte=last_week).count(),
                'monthly': Center.objects.filter(created_at__gte=last_month).count(),
            },
        },
        'activity_metrics': {
            'recent_logins': UserActivity.objects.filter(
                activity_type='login',
                timestamp__gte=last_week
            ).count(),
            'profile_updates': UserActivity.objects.filter(
                activity_type='profile_update',
                timestamp__gte=last_month
            ).count(),
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_data(request, data_type):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{data_type}_export.csv"'
    
    writer = csv.writer(response)
    
    if data_type == 'users':
        writer.writerow(['ID', 'Username', 'Email', 'Role', 'Status', 'Date Joined'])
        for user in User.objects.all():
            writer.writerow([
                user.id, user.username, user.email, user.role,
                user.status, user.date_joined
            ])
    elif data_type == 'centers':
        writer.writerow(['ID', 'Name', 'Address', 'Contact', 'Status'])
        for center in Center.objects.all():
            writer.writerow([
                center.id, center.name, center.address,
                center.contact_number, center.status
            ])
    
    return response