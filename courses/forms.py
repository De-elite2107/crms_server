from django import forms
from .models import *

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['course', 'resource_type', 'image', 'url', 'title', 'description']

class ResourceFileForm(forms.ModelForm):
    class Meta:
        model = ResourceFile
        fields = ['file']