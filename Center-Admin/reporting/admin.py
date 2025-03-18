from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('cell', 's_principle', 'submitted_by', 'status', 'created_at')
    list_filter = ('s_principle', 'status', 'created_at')
    search_fields = ('cell__name', 'submitted_by__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
