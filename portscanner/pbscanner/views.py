from django.shortcuts import render
from .forms import ScanForm
import socket

def can_connect_to_external_port(host, port):
    """Attempt to connect to an external host and port to see if it's accessible."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)  # Adjust timeout as needed
        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                return True  # Successfully connected
            else:
                return False  # Failed to connect
        except socket.error:
            return False  # Socket error occurred

def scan(request):
    message = ''
    form = ScanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        target = form.cleaned_data['target']
        port = form.cleaned_data['port']
        if can_connect_to_external_port(target, port):
            message = 'Connection successful. The port is open and accessible.'
        else:
            message = 'Failed to connect. The port is closed or not accessible.'

    return render(request, 'pbscanner/scan.html', {'form': form, 'message': message})