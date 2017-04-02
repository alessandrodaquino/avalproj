from django.shortcuts import render

def start(request):
    """start funcion, for main/welcome page"""
    return render(request, 'main.html', {})

