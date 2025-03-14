from django.db import models
from administration.models import Cell
from authentication.models import CustomUser

class Report(models.Model):
    S_PRINCIPLE_CHOICES = (
        ('1S', 'Sort'),
        ('2S', 'Set in Order'),
        ('3S', 'Shine'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name='reports')
    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submitted_reports')
    s_principle = models.CharField(max_length=2, choices=S_PRINCIPLE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='reports/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='reviewed_reports')
    review_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cell.name} - {self.s_principle} - {self.created_at.date()}"
