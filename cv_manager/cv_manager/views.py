# cv_manager/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Si vous avez un template 'home.html'
