from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from accounts.models import Profile

# ------------------- CREATE JOB -------------------
@login_required
def create_job(request):
    if request.user.profile.role != "employer":
        return redirect('dashboard')

    if request.method == "POST":
        Job.objects.create(
            employer=request.user,
            title=request.POST['title'],
            company=request.POST['company'],
            description=request.POST['description'],
            location=request.POST['location'],
            job_type=request.POST['job_type'],
            salary=request.POST['salary']
        )
        return redirect('employer_dashboard')

    return render(request, 'jobs/create_job.html')


# ------------------- LIST JOBS -------------------
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# ------------------- JOB DETAIL -------------------
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})


# ------------------- APPLY JOB -------------------
@login_required
def apply_job(request, job_id):
    profile = Profile.objects.get(user=request.user)

    if profile.role != "candidate":
        return redirect('dashboard')

    job = Job.objects.get(id=job_id)

    Application.objects.create(
        job=job,
        candidate=request.user,
        resume=profile.resume  # using resume from profile
    )

    return redirect('candidate_dashboard')


# ------------------- EMPLOYER: VIEW MY JOB POSTS -------------------
@login_required
def employer_job_posts(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'jobs/employer_job_posts.html', {'jobs': jobs})


# ------------------- CANDIDATE: MY APPLICATIONS -------------------
@login_required
def my_applications(request):
    apps = Application.objects.filter(candidate=request.user)
    return render(request, 'jobs/my_applications.html', {'applications': apps})

@login_required
def view_applications(request, job_id):
    profile = Profile.objects.get(user=request.user)

    # Only employer can see applicants
    if profile.role != "employer":
        return redirect('dashboard')

    job = Job.objects.get(id=job_id)

    # Ensure only job owner can view its applications
    if job.employer != request.user:
        return HttpResponse("Not allowed")

    applications = Application.objects.filter(job=job)

    return render(request, 'jobs/view_applications.html', {
        'job': job,
        'applications': applications
    })

