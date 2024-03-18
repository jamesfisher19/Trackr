from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Job
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect


import json

# HOME VIEW
def home(request):
    return render(request, 'pages/home.html')

# SIGN UP VIEW
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(reverse('tracker'))
        else:
            form = UserCreationForm()
        return render(request, 'pages/signup.html', {'form': form})
    


class CustomLoginView(LoginView):
    template_name = 'home.html'

# TRACKER VIEW
@login_required
def tracker(request):
    jobs = Job.objects.filter(user=request.user)
    companies = jobs.values_list('company_name', flat=True).distinct().order_by('company_name')
    print("TRACKER JOB COUNT:  ", jobs.count())
    for job in jobs:
        print(f"Job ID: {job.id}, Title: {job.position_title}, Company: {job.company_name}, Applied: {job.applied_status}")

    return render(request, 'pages/tracker.html', {'jobs': jobs, 'companies': companies})

# CREATE JOB VIEW
@login_required
def create_job(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        company_name = data.get('company_name')
        position_title = data.get('position_title')
        location = data.get('location')
        application_link = data.get('application_link')
        deadline = data.get('deadline')
        applied_status = data.get('applied_status') == 'True'

        # Create and save new job
        job = Job(user=user, company_name=company_name, position_title=position_title, location=location, application_link=application_link, deadline=deadline, applied_status=applied_status)
        job.save()
        print(f"New job created: {job.position_title} at {job.company_name}")

        job_dict = model_to_dict(job, fields=[field.name for field in job._meta.fields])
        job_dict['applied_status_display'] = job.get_applied_status_display()
        return JsonResponse({'status': 'success', 'job': job_dict})
    return render(request, 'pages/tracker.html')

# DELETE JOB VIEW
@login_required
def delete_job(request, job_id):
    job_to_delete = Job.objects.filter(pk=job_id, user=request.user).first()
    if job_to_delete:
        job_to_delete.delete()
    return HttpResponseRedirect(reverse('tracker'))

# FILTER JOBS VIEW
@login_required
def fetch_filtered_jobs(request):
    company_name = request.GET.get('company_name', '')
    applied_status = request.GET.get('applied_status', None)
    jobs = Job.objects.filter(user=request.user)
    # print("FILTER JOB COUNT: ", jobs.count())
    if company_name:
        jobs = jobs.filter(company_name__icontains=company_name)
    if applied_status == 'True':
        jobs = jobs.filter(applied_status=True)
    elif applied_status == 'False':
        jobs = jobs.filter(applied_status=False)

    from django.forms.models import model_to_dict
    jobs_list = [model_to_dict(job) for job in jobs]
    # print("JOBS LIST: ",jobs)
    # for job in jobs:
    #     print("Job:", job.company_name)
        
    return JsonResponse({'jobs': jobs_list})

# TEST VIEW
def my_view(request):
    print("Current user:", request.user.username)
    return render(request, 'pages/tracker.html')