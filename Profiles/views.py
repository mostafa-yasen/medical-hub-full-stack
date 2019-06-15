from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate


def loading(request):
    return render(request, 'loading.html')

def home(request):
    return render(request, 'landing.html')

def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)

        if user is None:
            # User not authenticated
            print('User not authenticated')
            return redirect('/')

        return redirect('/home/')

    return render(request, 'login.html')

def register(request):
    if request.POST:
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        confirm_email = request.POST['confirm_email']        
        phone = request.POST['phone']
        gender = request.POST['gender']
        user_type = request.POST['user_type']
        nid = request.POST['nid']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            # Password not match
            print('Password not match')
            return redirect('/')

        if email != confirm_email:
            # Email not match
            print('Email not match')
            return redirect('/')

        user = User.objects.create_user(
            first_name=fname,
            last_name=lname,
            password=password,
            email=email,
            username=email
        )

        user.profile.gender = gender
        if user_type == 'u':
            user.profile.is_doctor = False
        else:
            user.profile.is_doctor = True

        user.profile.nid = nid
        user.profile.phone = phone

        user.save()
        
        return redirect('/login/')
    
    return render(request, 'register.html')