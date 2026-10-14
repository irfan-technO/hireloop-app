from django.urls import path
from .views import *


urlpatterns =[
    path('add-resume/' ,  add_resume , name="add-resume"),
    path('update-resume/<int:pk>/' , update_resume , name='update-resume'),
    path ('resume-details/<int:pk>/',  resume_details , name= 'resume-details'),
    path('add-education/<int:pk>/' , add_education , name="add-education"),
    path(' update-education/<int:pk>/', update_education , name="update-education"),
    path('delete-education/<int:pk>/' , delete_education , name="delete-education"),
    path('add-work/<int:pk>/' , add_work ,  name="add-work"),
    path('update-work/<int:pk>/' , update_work , name='update-work'),
    path('delete-work/<int:pk>/' , update_work , name='delete-work')


]