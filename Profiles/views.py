from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from .models import Profile, Diagnose, Question
from django.http import JsonResponse

def loading(request):
    return render(request, 'loading.html')

def home(request):
    return render(request, 'landing.html')

def logout_view(request):
    logout(request)
    return redirect('/home/')

def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)

        if user is None:
            # User not authenticated
            print('=' * 50)
            print('User not authenticated')
            return redirect('/')


        login(request, user)
        print('login successful')
        return redirect('/communities/')

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
        # Set Gender
        user.profile.gender = gender

        # Set User Type
        print('=' * 50)
        print(user_type)
        if user_type == 'p':
            user.profile.is_doctor = False
        else:
            user.profile.is_doctor = True

        user.profile.nid = nid
        user.profile.phone = phone

        user.save()
        
        return redirect('/')
    
    return render(request, 'register.html')

@login_required
def profile(request):
    user = request.user
    context = {}

    if user.profile.is_doctor:
        template = 'doctor-profile.html'
        questions = Question.objects.filter(doctor=user.profile)
        context['questions'] = questions
    else:
        template = 'user-profile.html'
        diagnoses = Diagnose.objects.filter(patient=user)
        context['diagnoses'] = diagnoses

    return render(request , template, context=context)


@login_required
def users(request):
    template = 'users.html'

    all_users = User.objects.all()
    users = []

    for user in all_users:
        if not user.profile.is_doctor:
            users.append(user)

    context = {
        'users': users
    }

    return render(request, template, context=context)

@login_required
def users_details(request, user_id):
    template = 'user-details.html'
    user = User.objects.get(id=user_id)
    diagnoses = Diagnose.objects.filter(patient=user)

    context = {
        'user': user,
        'diagnoses': diagnoses
    }
    return render(request, template, context=context)

@login_required
def diagnose(request, user_id):
    doctor = request.user
    patient = User.objects.get(id=user_id)

    if not doctor.profile.is_doctor:
        return JsonResponse({'error':'user is not a doctor'})

    txtTitle = request.POST['txtTitle']
    txtContent = request.POST['txtContent']

    newDiagnose = Diagnose(
        patient=patient,
        doctor=doctor.profile,
        title=txtTitle,
        content=txtContent
    )

    print('=' * 50)
    print(newDiagnose)

    newDiagnose.save()

    return JsonResponse({'error':'None'})

@login_required
def doctors(request):
    template = 'doctors.html'

    all_users = User.objects.all()
    doctors = []

    for user in all_users:
        if user.profile.is_doctor:
            doctors.append(user)

    context = {
        'doctors': doctors
    }

    return render(request, template, context=context)

@login_required
def doctor_details(request, doctor_id):
    template = 'doctor-details.html'
    doctor = User.objects.get(id=doctor_id)

    questions = Question.objects.filter(doctor=doctor.profile)

    context = {
        'doctor': doctor,
        'questions': questions
    }

    return render(request, template, context)

@login_required
def ask(request, doctor_id):
    doctor = User.objects.get(id=doctor_id)
    patient = request.user

    content = request.POST['txtContent']
    print('=' * 50)
    print(content)
    print('=' * 50)
    if request.POST['anonymous']:
        anonymous = True
    else:
        anonymous = False

    newQuestion = Question(
        doctor=doctor.profile,
        patient=patient,
        content=content,
        anonymous=anonymous
    )
    newQuestion.save()

    return redirect('/')


@login_required
def answer(request, question_id):
    question = Question.objects.get(id=question_id)
    answer = request.POST['content']
    question.answer = answer
    question.save()

    return JsonResponse({'error': 'None'})

@login_required
def asked_questions(request):
    template = 'asked-questions.html'
    questions = Question.objects.filter(patient=request.user)

    context = {
        'questions': questions,
    }

    return render(request, template, context)