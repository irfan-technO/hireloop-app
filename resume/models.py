from django.db import models
from django.contrib.auth import get_user_model
import re

User  = get_user_model()

class Resume(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    state = models.CharField(
            max_length=100,
            choices=(
                ('Maharastra' , 'Maharastra'),
                ('Karnataka' , 'Karnataka')
            )
    
    )
    country = models.CharField(
            max_length=100,
            choices=(
                ('India' , 'india'),
            )
    )
    experience = models.CharField(
        max_length=20 ,
        choices=(
            ('1-3' , '1-3'),
            ('3-5' , '3-5'),
            ('5-10' , '5-10')
        )
    )
    age= models.PositiveIntegerField()
    gender = models.CharField(
        max_length=100 ,
        choices=(
            ('Male' , 'Male'),
            ('Female' , 'Female')
        )
    )
    language= models.CharField(
        max_length=100 ,
        choices=(
            ('English' , 'English'),
            ('Hindi' , 'Hindi')
           
        ),
        default='English'
    )
    education_level=models.CharField(
        max_length=100 ,
        choices=(
            ('None', "None"),
          ('Bachelors', 'Bachelors'),
        )
    )
    twitter = models.URLField(blank= True , null= True)
    linkedin = models.URLField( blank= True , null= True)
    about_candidate = models.TextField( blank= True , null= True)
    phone_number = models.CharField(max_length=15 , null= True)
    school_name = models.CharField(max_length=200 , null= True)
    video_link = models.URLField(null=True , blank=True)
    @property
    def embed_video_url(self):
        if not self.video_link:
            return ""
        
        url = self.video_link.strip()

        # Handle YouTube Shorts (e.g., youtube.com/shorts/VIDEO_ID)
        shorts_match = re.search(r"shorts/([a-zA-Z0-9_-]+)", url)
        if shorts_match:
            return f"https://www.youtube.com/embed/{shorts_match.group(1)}"

        # Handle Standard YouTube Watch Links (e.g., youtube.com/watch?v=VIDEO_ID)
        watch_match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
        if watch_match:
            return f"https://www.youtube.com/embed/{watch_match.group(1)}"

        # Handle Shortened YouTube Links (e.g., youtu.be/VIDEO_ID)
        youtu_match = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
        if youtu_match:
            return f"https://www.youtube.com/embed/{youtu_match.group(1)}"

        # Fallback if already an embed link
        return url

class Education(models.Model):
    resume = models.ForeignKey( Resume , on_delete=models.CASCADE)
    degree_type = models.CharField(
        max_length=20,
        choices=(
            ('Bacholers' , 'Bacholers'),
            ('Masters' , 'Masters'),
            ('Phd' , 'Phd')
        )
    )
    course = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    description = models.CharField()
    still_in_clg = models.CharField(
        max_length=20 ,
        choices=(
            ('Yes' ,'Yes'),
            ('No, i am passout' , 'No , i am passout')
        )
    )


class Work(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_set', null= True , blank=True)
    role = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    description = models.CharField()
    still_working_here = models.CharField(
        max_length=20 ,
        choices=(
            ('Yes' ,'Yes'),                           
            ('No ' , 'No') 
        ),
        default='No'
    )                                                                        