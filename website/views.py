from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from job.models import Job
from .models import ContactMessage

# Create your views here.
def home(request):
    jobs =  Job.objects.order_by('?')[:4] # only for small database
    context = {'jobs': jobs}
    return render(request , 'website/home.html' , context)
def about_us(request):
    return render(request , 'website/about_us.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            # Save message directly to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            messages.success(request, f"Thank you, {name}! Your message has been sent successfully.")
            return redirect('contact')
        else:
            messages.warning(request, "Please fill in all required fields.")

    return render(request, 'website/contact.html')
