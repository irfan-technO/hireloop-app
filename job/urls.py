from django.urls import path
from .views import *

urlpatterns = [
    path('create-job/', create_job, name="create-job"),
    path('update-job/<int:pk>/', update_job, name='update-job'),
    path('delete-job/<int:pk>/', delete_job, name='delete-job'),
    path('jobs-per-company/', jobs_per_company, name="jobs-per-company"),
    path('job-details/<int:pk>/', job_details, name='job-details'),
    
    # Job Responsibilities
    path('add-jobres/<int:pk>/', add_jobres, name='add-jobres'),
    path('edit-jobres/<int:pk>/', edit_jobres, name='edit-jobres'),
    path('delete-jobres/<int:pk>/', delete_jobres, name='delete-jobres'),
    
    # Job Experience / Skills
    path('add-jobexp/<int:pk>/', add_jobexp, name='add-jobexp'),
    path('edit-jobexp/<int:pk>/', edit_jobexp, name='edit-jobexp'),  # NEW
    path('delete-jobexp/<int:pk>/', delete_jobexp, name='delete-jobexp'),
    path('available-jobs' , available_jobs , name= 'available_jobs'),
    path('apply-to-job/<int:pk>/' , apply_to_job , name="apply_to_job"),
    path('save-job/<int:pk>/' , save_job , name= "save_job"),
    path('manage-applied-jobs/' , manage_applied_jobs , name="manage_applied_jobs"),
    path ("delete_application/<int:pk>/" , delete_application , name="delete_application"),
    path("applicants_per_job/<int:pk>/" , applicants_per_job , name="applicants_per_job"),
    path('accept_application/<int:pk>/' , accept_application , name="accept_application"),
    path("reject_application/<int:pk>/" , reject_application , name='reject_application'),
    path('all_saved_jobs/' , all_saved_jobs , name="all_saved_jobs"),
    path("delete_saved_job/<int:pk>/" , delete_saved_job , name = "delete_saved_job")

]