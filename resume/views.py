from django.shortcuts import render , redirect
from  django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from .form import *
from .models import *
from job.models import RecruiterMessage
from django.contrib.auth.decorators import login_required


User = get_user_model()
@login_required
def add_resume(request):
    # Prevent duplicate resume creation for the same user
    existing_resume = Resume.objects.filter(user=request.user).first()
    if existing_resume:
        messages.info(request, 'You already have a resume. Redirecting to update page.')
        # Uses your project's exact URL pattern name 'update resume'
        try:
            return redirect(reverse('update resume', kwargs={'pk': existing_resume.pk}))
        except Exception:
            try:
                return redirect(reverse('update-resume', kwargs={'pk': existing_resume.pk}))
            except Exception:
                return redirect('resume-details', pk=existing_resume.pk)

    if request.method == 'POST':
        form = AddResumeForm(request.POST, request.FILES)
        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.save()

            if hasattr(request.user, 'has_resume'):
                request.user.has_resume = True
                request.user.save()

            messages.success(request, 'You have successfully added your resume profile!')
            return redirect(reverse('resume-details', args=[var.pk]))
        else:
            messages.warning(request, 'Something went wrong, please check your form input.')
            context = {'form': form}
            return render(request, 'resume/add_resume.html', context)
    else:
        form = AddResumeForm()
        context = {'form': form}
        return render(request, 'resume/add_resume.html', context)
def update_resume(request , pk ):
    resume = Resume.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateResumeForm(request.POST , instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request , 'Resume information has been updated')
            return redirect(reverse('resume-details' , args=[resume.pk]))
        else:
            messages.error(request , 'Something went wrong , please try again')
            return redirect(reverse('resume=resume' , args=[resume.pk]))
    else:
        form= UpdateResumeForm(instance=resume)
        context = {'form': form } 
        return render(request , 'resume/update_resume.html' , context )   

def resume_details(request, pk):
    resume = Resume.objects.get(pk=pk)
    educations = resume.education_set.all().order_by('-end_year')
    works = resume.work_set.all().order_by('-end_year')

    if request.method == "POST" and request.user.is_authenticated:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        if name and email and message_text:
            RecruiterMessage.objects.create(
                recruiter=request.user,
                candidate_user=resume.user,
                name=name,
                email=email,
                message=message_text
            )
            messages.success(request, "Your message has been sent successfully to the candidate!")
            return redirect(reverse('resume details', args=[resume.pk]))
        else:
            messages.warning(request, "Please fill out all fields in the contact form.")

    context = {'resume': resume, 'educations': educations, 'works': works}
    return render(request, 'resume/resume_details.html', context)
def add_education(request, pk):
    resume = Resume.objects.get(pk=pk)
    if request.method == "POST":
        form = AddEducationForm(request.POST)
        if form.is_valid():
            # Update school_name on the Resume model
            resume.school_name = form.cleaned_data.get('school_name')
            resume.save()

            # Save education with commit=False to associate foreign key
            var = form.save(commit=False)
            var.resume = resume
            var.save()

            messages.success(request, "Education has been added to resume")
            return redirect(reverse('resume-details', args=[resume.pk]))
        else:
            messages.warning(request, "Something went wrong, please try again")
            return redirect(reverse('add-education', args=[resume.pk]))
    else:
        # Pre-populate school_name if already set on resume
        form = AddEducationForm(initial={'school_name': resume.school_name})

    context = {'form': form, 'resume': resume}
    return render(request, 'resume/add_education.html', context)

def  update_education(request ,pk):
   education = Education.objects.get(pk =pk)
   if request.method=="POST":
        form = UpdateEducationForm(request.POST , instance=education)
        if form.is_valid():
            form.save()
            messages.warning(request , 'Education details has been updated')
            return redirect(reverse('resume-details' , args=[education.resume.pk]))
        else:
           messages.warning(request , "Something went wrong , please try again")
           return redirect(reverse('update-education' , args=[education.pk]))
   else:
       form = UpdateEducationForm( instance= education)
       context = {'form':form}
       return  render(request , 'resume/update_education.html', context)

def delete_education(request , pk ):
    education = Education.objects.get(pk=pk)
    resume = Resume.objects.get(pk = education.resume.pk)
    education.delete()
    messages.success(request , "Education details has been deleted from your resume")
    return redirect( reverse( 'resume-details' , args=[resume.pk]))


def add_work(request , pk):
    resume = Resume.objects.get(pk=pk)
    if request.method =="POST":
        form = AddWorkForm(request.POST)
        if form.is_valid():
            var = form.save()
            var.resume = resume
            var.save()
            messages.success(request , "Work experience has been added to resume")
            return  redirect(reverse('add-education' , args=[resume.pk]))
        else:
            messages.warning(request , 'Something went wrong, please try again')
            return redirect(reverse('add-work' , args=[resume.pk]))
    else:
        form = AddWorkForm()
        context = {'form': form}
    return  render( request , 'resume/add_work.html' , context)    

def  update_work(request ,pk):
   work = Work.objects.get(pk =pk)
   if request.method=="POST":
        form = UpdateWorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            messages.success(request , 'Work experience details has been updated')
            return redirect(reverse('resume-details' , args=[work.resume.pk]))
        else:
           messages.warning(request , "Something went wrong , please try again")
           return redirect(reverse('update-work' , args=[work.pk]))
   else:
       form = UpdateWorkForm( instance= work)
       context = {'form':form}
       return  render(request , 'resume/update_work.html', context)

def delete_work(request , pk ):
    work =Work.objects.get(pk=pk)
    resume = Resume.objects.get(pk = work.resume.pk)
    work.delete()
    messages.success(request , "Work experience  details has been deleted from your resume")
    return redirect( reverse( 'resume-details' , args=[resume.pk]))