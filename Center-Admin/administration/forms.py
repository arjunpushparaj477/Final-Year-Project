from django import forms
from .models import Zone
from authentication.models import CustomUser

class ZoneForm(forms.ModelForm):
    zone_leader = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='zone_leader'),
        required=False,
        empty_label="Select Zone Leader"
    )

    class Meta:
        model = Zone
        fields = ['name', 'description', 'zone_leader']