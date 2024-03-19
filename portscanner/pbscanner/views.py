from django.shortcuts import render
from .forms import ScanForm
import socket

def is_open_tcp(ip, port):
    print(f"Checking TCP port: {ip}:{port}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            result = sock.connect_ex((ip, port))
            print(f"connect_ex result: {result}")
            return result == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def scan(request):
    message = ''
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            port = form.cleaned_data['port']
            if is_open_tcp(target, port):
                message = 'Good to go! RCON port is accessable.'
            else:
                message = 'RCON port is closed or not accessible.'
    else:
        form = ScanForm()

    return render(request, 'pbscanner/scan.html', {'form': form, 'message': message})