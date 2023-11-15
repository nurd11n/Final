from django import forms
from django.forms import ModelForm
from .models import *


class DistanceForm(ModelForm):
    from_location = forms.ModelChoiceField(label="Location from", required=True, queryset=Locations.objects.all())
    to_location = forms.ModelChoiceField(label="Location to", required=True, queryset=Locations.objects.all())

    class Meta:
        model = Distances
        exclude = ['created_at', 'edited_at', 'distance_km','duration_mins','duration_traffic_mins']
