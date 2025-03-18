from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp

class User(AbstractUser):
    # ... existing fields ...
    
    two_factor_secret = models.CharField(max_length=32, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def enable_2fa(self):
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()
            self.two_factor_enabled = True
            self.save()
        return self.two_factor_secret

    def verify_2fa(self, code):
        if self.two_factor_enabled:
            totp = pyotp.TOTP(self.two_factor_secret)
            return totp.verify(code)
        return True