from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddCompanyForm, UpdateCompanyForm
from .models import Company

def add_company(request):
    if request.method == "POST":
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.user = request.user
            var.save()
            request.user.has_company = True
            request.user.save()

            messages.success(request, "Your company information has been added and saved")
            return redirect('dashboard')
        else:
            print("ADD FORM ERRORS:", form.errors)
            messages.error(request, "Form validation failed.")
            return redirect('add-company')
    else:
        form = AddCompanyForm()
        context = {'form': form}
        return render(request, 'company/add_company.html', context)


def update_company(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        form = UpdateCompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company information updated successfully!")
            return redirect('update-company', pk=company.pk)
        else:
            print("UPDATE FORM ERRORS:", form.errors)
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = UpdateCompanyForm(instance=company)

    context = {
        'form': form,
        'company': company
    }
    return render(request, 'company/update_company.html', context)


def company_details(request, pk):
    company = get_object_or_404(Company, pk=pk)
    context = {'company': company}
    return render(request, 'company/company_details.html', context)