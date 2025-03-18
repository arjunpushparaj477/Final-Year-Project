from django.db import models
from accounts.models import User

class Center(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='administered_centers')
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name