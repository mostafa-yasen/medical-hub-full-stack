from django.shortcuts import render


def loading(request):
    return render(request, 'loading.html')

def home(request):
    return render(request, 'landing.html')