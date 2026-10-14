from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from .form import RegisterUserForm, UserPasswordChangeForm, UpdateProfileForm
import random
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


def register_candidate(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # Store valid registration data in session temporarily
            request.session['reg_data'] = {
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'email': form.cleaned_data.get('email'),
                'password': form.cleaned_data.get('password1'),
                'is_candidate': True,
                'is_recruiter': False,
            }

            # Generate 6-Digit OTP
            otp = str(random.randint(100000, 999999))
            request.session['reg_otp'] = otp

            # Debug print to terminal
            print("\n" + "="*40)
            print(f" REGISTRATION OTP FOR {form.cleaned_data.get('email')}: {otp}")
            print("="*40 + "\n")

            # Send OTP email
            try:
                send_mail(
                    subject="Hireloop - Account Registration OTP",
                    message=f"Hello {form.cleaned_data.get('first_name')},\n\nYour OTP to verify your candidate account registration is: {otp}\n\nDo not share this OTP with anyone.",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@hireloop.com'),
                    recipient_list=[form.cleaned_data.get('email')],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email delivery error: {e}")

            messages.success(request, f"OTP sent to {form.cleaned_data.get('email')}. Please verify to complete registration.")
            return redirect('verify_registration_otp')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'accounts/register_candidate.html', context)

def register_recruiter(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # Store valid registration data in session temporarily
            request.session['reg_data'] = {
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'email': form.cleaned_data.get('email'),
                'password': form.cleaned_data.get('password1'),
                'is_candidate': False,
                'is_recruiter': True,
            }

            # Generate 6-Digit OTP
            otp = str(random.randint(100000, 999999))
            request.session['reg_otp'] = otp

            # Debug print to terminal
            print("\n" + "="*40)
            print(f" REGISTRATION OTP FOR {form.cleaned_data.get('email')}: {otp}")
            print("="*40 + "\n")

            # Send OTP email
            try:
                send_mail(
                    subject="Hireloop - Recruiter Registration OTP",
                    message=f"Hello {form.cleaned_data.get('first_name')},\n\nYour OTP to verify your recruiter account registration is: {otp}\n\nDo not share this OTP with anyone.",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@hireloop.com'),
                    recipient_list=[form.cleaned_data.get('email')],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email delivery error: {e}")

            messages.success(request, f"OTP sent to {form.cleaned_data.get('email')}. Please verify to complete registration.")
            return redirect('verify_registration_otp')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'accounts/register_recruiter.html', context)

def verify_registration_otp(request):
    reg_data = request.session.get('reg_data')
    saved_otp = request.session.get('reg_otp')

    if not reg_data or not saved_otp:
        messages.warning(request, "Please fill out the registration form first.")
        return redirect('register_candidate')

    if request.method == "POST":
        user_otp = request.POST.get('otp', '').strip()

        if user_otp == saved_otp:
            # Create user account after OTP verification
            email = reg_data['email']
            user = User.objects.create_user(
                username=email,
                email=email,
                password=reg_data['password'],
                first_name=reg_data['first_name'],
                last_name=reg_data['last_name']
            )
            user.is_candidate = reg_data['is_candidate']
            user.is_recruiter = reg_data['is_recruiter']
            user.save()

            # Clear session data
            request.session.pop('reg_data', None)
            request.session.pop('reg_otp', None)

            role_title = "Candidate" if user.is_candidate else "Recruiter"
            messages.success(request, f"{role_title} account created successfully! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP code. Please try again.")

    return render(request, 'accounts/verify_registration_otp.html', {'email': reg_data.get('email')})


def login_user(request):
    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        identifier = request.POST.get('username')  # Accepts email or username input
        password = request.POST.get('password')

        user = authenticate(request, username=identifier, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None and user.is_active:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid email or password. Please try again.')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('login')


@login_required
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was changed successfully!')
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong. Please check the errors below.')
    else:
        form = UserPasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


@login_required
def update_profile(request, pk):
    user = User.objects.get(pk=pk)

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your information is now updated")
            return redirect(reverse('update-profile', args=[user.pk]))
        else:
            messages.warning(request, "Something went wrong, please try again")
    else:
        form = UpdateProfileForm(instance=user)

    context = {'form': form}
    return render(request, 'accounts/update_profile.html', context)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        user = User.objects.filter(email=email).first() or User.objects.filter(username=email).first()
        
        if user:
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Save OTP & Email securely in user session
            request.session['reset_email'] = user.email
            request.session['reset_otp'] = otp

            # Debug print so you can always see the OTP in VS Code Terminal
            print("\n" + "="*40)
            print(f" GENERATED OTP FOR {user.email}: {otp}")
            print("="*40 + "\n")
            
            # Send OTP email
            try:
                send_mail(
                    subject="Hireloop - Password Reset OTP",
                    message=f"Hello {user.first_name or 'User'},\n\nYour OTP to reset your Hireloop account password is: {otp}\n\nDo not share this OTP with anyone.",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@hireloop.com'),
                    recipient_list=[user.email],
                    fail_silently=False,  # Set to False so SMTP errors show in console if credentials fail
                )
            except Exception as e:
                print(f"Email delivery error: {e}")

            messages.success(request, f"OTP sent to {user.email}. Check your inbox.")
            return redirect('verify_otp')
        else:
            messages.error(request, "No account found with this email address.")
            
    return render(request, 'accounts/forgot_password.html')

def verify_otp(request):
    # Ensure user initiated forgot password
    if 'reset_otp' not in request.session:
        messages.warning(request, "Please request a password reset first.")
        return redirect('forgot_password')

    if request.method == "POST":
        user_otp = request.POST.get('otp', '').strip()
        saved_otp = request.session.get('reset_otp')

        if user_otp == saved_otp:
            request.session['otp_verified'] = True
            messages.success(request, "OTP verified successfully. Enter your new password.")
            return redirect('reset_password_confirm')
        else:
            messages.error(request, "Invalid OTP code. Please try again.")

    return render(request, 'accounts/verify_otp.html')


def reset_password_confirm(request):
    if not request.session.get('otp_verified'):
        messages.warning(request, "Unauthorized access. Please verify your OTP first.")
        return redirect('forgot_password')

    if request.method == "POST":
        pass1 = request.POST.get('password1', '').strip()
        pass2 = request.POST.get('password2', '').strip()

        if pass1 and pass2 and pass1 == pass2:
            email = request.session.get('reset_email')
            user = User.objects.filter(email=email).first()
            
            if user:
                user.set_password(pass1)
                user.save()
                
                # Clear reset session data
                request.session.pop('reset_email', None)
                request.session.pop('reset_otp', None)
                request.session.pop('otp_verified', None)

                messages.success(request, "Password reset successfully! Please log in with your new password.")
                return redirect('login')
            else:
                messages.error(request, "User account error. Try again.")
        else:
            messages.error(request, "Passwords do not match or are invalid.")

    return render(request, 'accounts/reset_password.html')