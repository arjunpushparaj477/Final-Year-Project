from django.urls import path
from .views import (AdminDashboardView, UserListView, ZoneListView, 
                   CellListView, ReportListView, ZoneCreateView,
                   UserCreateView, UserEditView, UserDeleteView)  # Add UserDeleteView here

app_name = 'administration'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('zones/', ZoneListView.as_view(), name='zone_list'),
    path('zones/create/', ZoneCreateView.as_view(), name='zone_create'),  # Add this line
    path('cells/', CellListView.as_view(), name='cell_list'),
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserEditView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),  # Add this line
]