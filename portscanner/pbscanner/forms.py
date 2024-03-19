from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError
import socket

def validate_ip_or_url(value):
    # Attempt to validate as IP
    try:
        socket.inet_aton(value)
        return
    except socket.error:
        pass

    # Ensure the value has a scheme for URL validation
    if not (value.startswith('http://') or value.startswith('https://')):
        value = 'http://' + value

    # Attempt to validate as URL
    validator = URLValidator()
    try:
        validator(value)
    except DjangoValidationError:
        raise ValidationError("Please enter a valid IP address or URL.")

class ScanForm(forms.Form):
    target = forms.CharField(label='IP Address / URL', validators=[validate_ip_or_url], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 192.168.1.1 or example.com'}))
    port = forms.IntegerField(label='Port', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 27016'}), min_value=1, max_value=65535)