from django.db import models
from django.conf import settings
from authentication.models import CustomUser  # Add this import

class Zone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    zone_leader = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='managed_zones')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cell(models.Model):
    name = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='cells')
    cell_leader = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='managed_cells')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.zone.name}"


class Report(models.Model):
    REPORT_STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='reports')
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name='reports')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_reports')
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 5S Categories
    sort_score = models.IntegerField(default=0)
    set_in_order_score = models.IntegerField(default=0)
    shine_score = models.IntegerField(default=0)
    standardize_score = models.IntegerField(default=0)
    sustain_score = models.IntegerField(default=0)
    
    comments = models.TextField(blank=True)
    improvement_suggestions = models.TextField(blank=True)
    attachments = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.zone.name} - {self.created_at.date()}"

    def get_total_score(self):
        return (self.sort_score + self.set_in_order_score + 
                self.shine_score + self.standardize_score + 
                self.sustain_score)

    class Meta:
        ordering = ['-created_at']
