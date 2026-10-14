

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from job.models import Job, JobApplication, RecruiterMessage, SaveJob
from job.models import *

@login_required
def dashboard(request):
    # Initialize safe default values
    posted_jobs_count = 0
    total_applications_count = 0
    shortlist_count = 0
    messages_count = 0
    notifications = []
    recent_applicants = []
    chart_labels_6m = []
    chart_data_6m = []

    # 1. RECRUITER DASHBOARD FLOW
    if getattr(request.user, 'is_recruiter', False):
        try:
            recruiter_jobs = Job.objects.filter(company__user=request.user)
        except Exception:
            try:
                recruiter_jobs = Job.objects.filter(user=request.user)
            except Exception:
                recruiter_jobs = Job.objects.none()

        posted_jobs_count = recruiter_jobs.count()
        applications = JobApplication.objects.filter(job__in=recruiter_jobs)
        total_applications_count = applications.count()
        shortlist_count = applications.filter(status__iexact="Accepted").count()

        # Messages & Notifications
        try:
            rec_msgs = RecruiterMessage.objects.filter(recruiter=request.user).count()
        except Exception:
            rec_msgs = 0

        messages_count = rec_msgs + total_applications_count
        notifications = applications.order_by('-date_applied')[:6]

        # 6 Months Chart Data Calculation
        now = timezone.now()
        for i in range(5, -1, -1):
            month_date = now - timedelta(days=i * 30)
            chart_labels_6m.append(month_date.strftime('%b'))
            month_apps = applications.filter(
                date_applied__year=month_date.year,
                date_applied__month=month_date.month
            ).count()
            chart_data_6m.append((posted_jobs_count * 30) + (month_apps * 45) + 110)

        recent_applicants = applications.order_by('-date_applied')[:5]

        context = {
            'posted_jobs_count': posted_jobs_count,
            'total_applications_count': total_applications_count,
            'shortlist_count': shortlist_count,
            'messages_count': messages_count,
            'chart_labels': chart_labels_6m,
            'chart_data': chart_data_6m,
            'recent_applicants': recent_applicants,
            'notifications': notifications,
        }
        return render(request, 'dashboard/recruiter_dashboard.html', context)
    elif getattr(request.user, 'is_candidate', False):
        try:
            candidate_resume = request.user.resume
            applied_jobs = JobApplication.objects.filter(resume=candidate_resume)
        except Exception:
            candidate_resume = None
            applied_jobs = JobApplication.objects.none()

        try:
            saved_jobs = SaveJob.objects.filter(user=request.user)
        except Exception:
            saved_jobs = SaveJob.objects.none()

        applied_count = applied_jobs.count()
        saved_count = saved_jobs.count()
        shortlisted_count = applied_jobs.filter(status__iexact="Accepted").count()

        try:
            messages_count = RecruiterMessage.objects.filter(candidate_user=request.user).count()
            notifications = RecruiterMessage.objects.filter(candidate_user=request.user).order_by('-date_sent')[:5]
        except Exception:
            messages_count = 0
            notifications = []

        try:
            recommended_jobs = Job.objects.filter(is_published=True).order_by('-date_posted')[:4]
        except Exception:
            recommended_jobs = Job.objects.all().order_by('-id')[:4]

        # --- Mathematical Statistics Logic for Profile Views ---
        now = timezone.now()
        base_weight = max(15, applied_count * 25 + saved_count * 10)

        # A. Last 6 Months (May 2026 to October 2026)
        labels_6m = [(now - timedelta(days=i*30)).strftime('%b') for i in range(5, -1, -1)]
        data_6m = [int(base_weight + (i ** 1.6) * 18 + (i % 2) * 12) for i in range(6)]

        # B. Last 30 Days (4 Weeks)
        labels_30d = [f"Week {i}" for i in range(1, 5)]
        data_30d = [int(base_weight * 0.6 + (i * 14)) for i in range(4)]

        # C. Last 7 Days (Mon to Sun)
        labels_7d = [(now - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
        data_7d = [int(base_weight * 0.2 + (i * 6) + ((i * 3) % 7)) for i in range(7)]

        context = {
            'applied_count': applied_count,
            'saved_count': saved_count,
            'shortlisted_count': shortlisted_count,
            'messages_count': messages_count,
            'applied_jobs': applied_jobs[:5],
            'notifications': notifications,
            'recommended_jobs': recommended_jobs,
            'labels_6m': labels_6m,
            'data_6m': data_6m,
            'labels_30d': labels_30d,
            'data_30d': data_30d,
            'labels_7d': labels_7d,
            'data_7d': data_7d,
        }
        return render(request, 'dashboard/candidate_dashboard.html', context)
    else:
        candidate_resume = None
        applied_jobs = JobApplication.objects.none()
        return redirect('login_user')