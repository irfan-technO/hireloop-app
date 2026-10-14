from django.urls import path
from .views import *

urlpatterns = [
    path('register_candidate/', register_candidate, name="register_candidate"),
    path('register_recruiter/', register_recruiter, name="register_recruiter"),
    path('login/', login_user, name="login"),
    path('logout_user/', logout_user, name="logout"),
    path('change_password', change_password, name='change_password'),
    path('update_profile/<int:pk>/', update_profile, name='update-profile'),
    path('verify_registration_otp/', verify_registration_otp, name="verify_registration_otp"),
    
    # Forgot Password OTP Routes
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password_confirm, name='reset_password_confirm'),

]