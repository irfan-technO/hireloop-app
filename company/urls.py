from django.urls import path
from .views import *


urlpatterns = [
    path('add-company/' , add_company , name="add-company"),
    path('update-company/<int:pk>/' , update_company , name= "update-company"),
    path('company-details/<int:pk>/', company_details , name="company-details" )
]
