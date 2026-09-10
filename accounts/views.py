from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from jobs.models import Job, Application

# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.get(user=user)
        profile.role = role

        if role == 'candidate' and 'resume' in request.FILES:
            profile.resume = request.FILES['resume']

        profile.save()

        return redirect('login')

    return render(request, 'accounts/register.html')


# ---------------- LOGIN ----------------
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {"error": "Invalid credentials"})

    return render(request, 'accounts/login.html')


# ---------------- LOGOUT ----------------
def logout_user(request):
    logout(request)
    return redirect('login')


# ---------------- DASHBOARD REDIRECT ----------------
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == "employer":
        return redirect('employer_dashboard')
    else:
        return redirect('candidate_dashboard')


# ---------------- EMPLOYER DASHBOARD ----------------
@login_required
def employer_dashboard(request):
    if request.user.profile.role != "employer":
        return redirect('dashboard')
    return render(request, 'accounts/employer_dashboard.html')


# ---------------- CANDIDATE DASHBOARD ----------------
@login_required
def candidate_dashboard(request):
    if request.user.profile.role != "candidate":
        return redirect('dashboard')
    return render(request, 'accounts/candidate_dashboard.html')
