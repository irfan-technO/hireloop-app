
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Company(models.Model):
    STATE_CHOICES = (
        ('Maharastra', 'Maharastra'),
        ('Karnataka', 'Karnataka'),
    )

    COUNTRY_CHOICES = (
        ('India', 'India'),
    )

    INDUSTRY_CHOICES = (
        ('Software', 'Software'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
    )

    SIZE_CHOICES = (
        ('1-15', '1-15'),
        ('15-40', '15-40'),
        ('40-70', '40-70'),
        ('70-100', '70-100'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    primary_industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField(max_length=250)
    website = models.URLField(max_length=200, blank=True, null=True)
    company_size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    founded_in = models.PositiveIntegerField()
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    about_company = models.TextField()

    def __str__(self):
        return self.name

