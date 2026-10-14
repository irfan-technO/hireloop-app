from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404 
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from .forms import*
from .models import*
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from company.models import Company
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
User = get_user_model()

def create_job(request):
    if request.method == 'POST':
        form = CreateJobForms(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            # Assign the logged-in user's company instance
            var.company = request.user.company  
            var.save()
            messages.success(request, "New Job has been created and saved , please add other requirements")
            return redirect( reverse( 'job-details' , args=[var.pk]))
        else:
            messages.warning(request, "Something went wrong, please try again")
            return redirect('create-job')
    else:
        form = CreateJobForms()
    
    context = {'form': form}
    return render(request, 'job/create_job.html', context)

def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job information has been updated')
            return redirect('jobs-per-company')
    else:
        form = UpdateJobForm(instance=job)

    context = {
        'form': form,
        'job': job
    }
    return render(request, 'job/update_job.html', context)
      
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.delete()
    messages.success(request, "Job has been deleted successfully.")
    return redirect('jobs-per-company')


def jobs_per_company(request):
    company = Company.objects.get(pk=request.user.company.pk)
    jobs = company.job_set.all()
    
    context = {'jobs': jobs, 'company': company}
    return render(request, 'job/jobs_per_company.html', context)


def job_details(request, pk):
    job = get_object_or_404(Job, pk=pk)
    company = job.company
    
    # Fetch other jobs posted by the same company excluding the current job
    other_jobs = Job.objects.filter(company=company).exclude(pk=job.pk)
    jobs = company.job_set.all()[:3]
    
    context = {
        'job': job,
        'company': company,
        'other_jobs': other_jobs,
        "jobs": jobs
    }
    return render(request, 'job/job_details.html', context)
def add_jobres(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        form = AddJobRes(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.job = job
            var.save()
            messages.success(request, 'New job responsibility has been added to job details.')
            return redirect(reverse('add-jobres', args=[job.pk]))
        else:
            messages.warning(request, "Something went wrong, please try again.")
    else:
        form = AddJobRes()

    context = {'form': form, 'job': job}
    return render(request, 'job/add_jobres.html', context)


def edit_jobres(request, pk):
    jobres = get_object_or_404(JobRes, pk=pk)
    job = jobres.job
    if request.method == "POST":
        form = AddJobRes(request.POST, instance=jobres)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job responsibility updated successfully.')
            return redirect(reverse('job-details', args=[job.pk]))
        else:
            messages.warning(request, "Something went wrong, please try again.")
    else:
        form = AddJobRes(instance=jobres)

    context = {'form': form, 'job': job, 'is_edit': True}
    return render(request, 'job/add_jobres.html', context)


def delete_jobres(request, pk):
    jobres = get_object_or_404(JobRes, pk=pk)
    get_job = jobres.job
    jobres.delete()
    messages.success(request, 'Job responsibility has been deleted from job.')
    return redirect(reverse('job-details', args=[get_job.pk]))


def add_jobexp(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        form = AddJobExp(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.job = job
            var.save()
            messages.success(request, 'New job experience has been added to job details.')
            return redirect(reverse('add-jobexp', args=[job.pk]))
        else:
            messages.warning(request, "Something went wrong, please try again.")
    else:
        form = AddJobExp()

    context = {'form': form, 'job': job}
    return render(request, 'job/add_jobexp.html', context)


def edit_jobexp(request, pk):
    jobexp = get_object_or_404(JobExp, pk=pk)
    job = jobexp.job
    if request.method == "POST":
        form = AddJobExp(request.POST, instance=jobexp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job experience updated successfully.')
            return redirect(reverse('job-details', args=[job.pk]))
        else:
            messages.warning(request, "Something went wrong, please try again.")
    else:
        form = AddJobExp(instance=jobexp)

    context = {'form': form, 'job': job, 'is_edit': True}
    return render(request, 'job/add_jobexp.html', context)


def delete_jobexp(request, pk):
    jobexp = get_object_or_404(JobExp, pk=pk)
    get_job = jobexp.job
    jobexp.delete()
    messages.success(request, 'Job experience has been deleted from job.')
    return redirect(reverse('job-details', args=[get_job.pk]))

def available_jobs(request):
    # 1. Fetch base active jobs
    jobs_list = Job.objects.filter(status="Active").order_by('-date_time_posted')

    # 2. Extract GET filter parameters
    search = request.GET.get('search', '').strip()
    job_location = request.GET.get('job_location', '').strip()
    job_type = request.GET.get('job_type', '').strip()
    job_cat = request.GET.get('job_cat', '').strip()
    pay_mode = request.GET.get('pay_mode', '').strip()

    # 3. Apply filters BEFORE paginating
    if search:
        jobs_list = jobs_list.filter(title__icontains=search)
    if job_location:
        jobs_list = jobs_list.filter(job_location__iexact=job_location)
    if job_type:
        jobs_list = jobs_list.filter(job_type__iexact=job_type)
    if job_cat:
        jobs_list = jobs_list.filter(job_cat__iexact=job_cat)
    if pay_mode:
        jobs_list = jobs_list.filter(pay_mode__iexact=pay_mode)

    # 4. Paginate results (3 jobs per page to demonstrate pagination)
    paginator = Paginator(jobs_list, 4)
    page_number = request.GET.get('page')
    
    try:
        jobs = paginator.page(page_number)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    context = {
        'jobs': jobs,
        'search': search,
        'selected_location': job_location,
        'selected_type': job_type,
        'selected_cat': job_cat,
        'selected_pay_mode': pay_mode,
    }
    return render(request, 'job/available_jobs.html', context)

def apply_to_job( request , pk ):
    job = Job.objects.get(pk=pk)
    check_application = job.jobapplication_set.filter(job= job , resume = request.user.resume).exists()

    if job.status == "Active":
        if request.user.has_resume:
            if not check_application:
                JobApplication.objects.create(
                    job = job , resume= request.user.resume
                )
                messages.success(request , 'You have successfully applied to this job! You can see progress in Dashboard')
                return redirect(reverse('job-details' , args=[job.pk]))
            else:
                messages.warning(request , 'You have already applied to this job!')
                return redirect(reverse('job-details' , args=[job.pk]))
        else:
            messages.warning(request , "You do not hava a Resume , Please create one to apply")
            return redirect(reverse('job-details' , args=[job.pk]))
    else:
        messages.warning(request , "This job is no longer active")
        return redirect(reverse('job-details' , args=[job.pk]))

    

def save_job( request , pk ):
    job = Job.objects.get(pk=pk)
    check_instance = job.savejob_set.filter(job=job , resume= request.user.resume).exists()

    if not check_instance:
        SaveJob.objects.create(job=job , resume = request.user.resume)
        messages.success(request , "You just sucessfully saved this job!")
        return redirect(reverse('job-details' , args=[job.pk]))
    else:
        messages.warning(request ,"You have already saved this job ")
        return redirect(reverse('job-details' , args=[job.pk]))
        


def manage_applied_jobs(request):
    jobs = JobApplication.objects.filter(resume = request.user.resume)
    context = {'jobs': jobs} 
    return render(request , 'job/manage_applied_jobs.html' , context)           

def delete_application(request , pk ):
    job_application  = JobApplication.objects.get(pk=pk)
    job_application.delete()
    messages.success( request , 'You have deleted  the job application')
    return redirect('manage_applied_jobs')


def applicants_per_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Base QuerySet
    # Base QuerySet
    applicants_list = job.jobapplication_set.all()

    # Header Statistics
    total_count = applicants_list.count()
    approved_count = applicants_list.filter(status__iexact="Accepted").count()
    rejected_count = applicants_list.filter(status__iexact="Declined").count()

    # 1. Filter by Status Dropdown
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        applicants_list = applicants_list.filter(status__iexact=status_filter)

    # 2. Filter by Date Range
    date_filter = request.GET.get('date_range', 'all')
    now = timezone.now()

    if date_filter == '7_days':
        applicants_list = applicants_list.filter(date_applied__gte=now - timedelta(days=7))
    elif date_filter == '30_days':
        applicants_list = applicants_list.filter(date_applied__gte=now - timedelta(days=30))
    elif date_filter == 'today':
        applicants_list = applicants_list.filter(date_applied=timezone.now().date())

    # 3. Search Query
    search_query = request.GET.get('q', '').strip()
    if search_query:
        applicants_list = applicants_list.filter(
            Q(resume__user__first_name__icontains=search_query) |
            Q(resume__user__last_name__icontains=search_query) |
            Q(resume__user__username__icontains=search_query)
        )

    context = {
        'job': job,
        'applicants': applicants_list,
        'total': total_count,
        'approved': approved_count,
        'rejected': rejected_count,
        'current_status': status_filter,
        'current_date': date_filter,
        'search_query': search_query,
    }
    return render(request, 'job/applicants_per_job.html', context)

def  accept_application(request , pk):
     application = JobApplication.objects.get(pk=pk)
     application.status = "Accepted"
     application.save()
     messages.success(request , 'You have accepted this candidate')
     return redirect(reverse('applicants_per_job' , args=[application.job.pk]))

def  reject_application(request , pk):
     application = JobApplication.objects.get(pk=pk)
     application.status = "Declined"
     application.save()
     messages.success(request , 'You have  rejected this candidate')
     return redirect(reverse('applicants_per_job' , args=[application.job.pk]))

def all_saved_jobs(request):
    jobs = SaveJob.objects.filter(resume = request.user.resume)
    context = {'jobs': jobs}
    return render(request , 'job/all_saved_jobs.html' , context)

def delete_saved_job(request , pk):
    job = SaveJob.objects.get(pk=pk)
    job.delete()
    messages.success(request,"Saved job has been removed from your dashboard")
    return redirect('all-saved-jobs')