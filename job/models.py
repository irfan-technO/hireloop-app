from django.db import models
from django.contrib.auth import get_user_model
from company.models import Company
from resume.models import Resume
from core import settings
User = get_user_model

class Job(models.Model):
    company= models.ForeignKey(Company , on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    date_time_posted = models.DateTimeField(auto_now_add= True)
    date_posted = models.DateField(auto_now_add= True)
    pay = models.CharField(max_length=50)
    pay_mode = models.CharField(
        max_length=20,
        choices= (
            ('Daily' , 'Daily'),
            ('Weekly' , 'Weekly'),
            ('Monthly' ,'Monthly')
        )
    )
    job_type = models.CharField(
        max_length=50 ,
        choices=(
            ('Part Time' ,'Part Time'),
            ( 'Full Time','Full Time') 
            
        )
    )
    job_location =models.CharField(
        max_length=30 ,
        choices=(
          ('Remote' , 'Remote'),
          ('Hybrid' , 'Hybrid'),
          ( 'On site' , 'On site')
        )
    )
    job_cat = models.CharField(
        max_length= 20 ,
        choices=(
            ('Permanant' , 'Permanant'),
            ('Contract' , 'Contract')
        )
    ) 
    expiry_date = models.DateField(null=True)
    hours_per_week = models.PositiveIntegerField()
    job_description = models.TextField()
    is_published = models.BooleanField(default=False)
    status = models.CharField(
        max_length=40 ,
        choices=(
            ('Pending' , "Pending"),
            ('Active' , "Active"),
            ("Expired" , "Expired")
        ),
        default='Pending'
    )

#Job Responsibility
class JobRes(models.Model):
    job = models.ForeignKey( Job , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

#Job Exprience 
class JobExp(models.Model):
    job = models.ForeignKey(Job  , on_delete=models.CASCADE)
    name = models.CharField(max_length=300)

class JobApplication(models.Model):
    resume = models.ForeignKey(Resume  , on_delete= models.CASCADE)
    job = models.ForeignKey( Job , on_delete= models.CASCADE)
    date_time_applied = models.DateTimeField(auto_now_add= True)
    date_applied = models.DateField(auto_now_add= True)
    status = models.CharField(
        max_length=100 ,
        choices=(
            ('Pending', 'Pending'),
            ('Accepted' , 'Accepted'),
            ('Declined' , 'Declined')
        ) ,
        default= 'Pending'
    )

class SaveJob(models.Model):
     resume = models.ForeignKey(Resume  , on_delete= models.CASCADE)
     job = models.ForeignKey( Job , on_delete= models.CASCADE)
     date_time_saved = models.DateTimeField(auto_now_add= True)
     date_saved = models.DateField(auto_now_add= True)

class RecruiterMessage(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    candidate_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} to {self.candidate_user.email}"