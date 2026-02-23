from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
# authsystem/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'authsystem/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'authsystem/login.html')



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import UserOTP

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password']

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # Create inactive user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        UserOTP.objects.create(user=user, otp=otp)

        # Send OTP Email
        send_mail(
            subject="Your OTP for StockPredictor",
            message=f"Hello {username},\n\nYour OTP is: {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        # Store user ID in session
        request.session['user_id'] = user.id
        return redirect('verify_otp')

    return render(request, 'authsystem/register.html')


from django.contrib.auth import login
from .models import UserOTP

def verify_otp(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect('register')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        input_otp = request.POST['otp']
        real_otp = UserOTP.objects.get(user=user).otp

        if input_otp == real_otp:
            user.is_active = True
            user.save()
            UserOTP.objects.get(user=user).delete()  # delete OTP after use
            messages.success(request, "OTP verified successfully! You can now login.")
            return redirect('login')
        else:
            messages.error(request, "Incorrect OTP. Please try again.")

    return render(request, 'authsystem/verify_otp.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect('forgot_password')

        otp = str(random.randint(100000, 999999))
        UserOTP.objects.update_or_create(user=user, defaults={'otp': otp})

        send_mail(
            subject="Password Reset OTP",
            message=f"Hello {user.username}, your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        request.session['reset_user_id'] = user.id
        return redirect('reset_verify_otp')

    return render(request, 'authsystem/forgot_password.html')


def reset_verify_otp(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired.")
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        input_otp = request.POST['otp']
        real_otp = UserOTP.objects.get(user=user).otp

        if input_otp == real_otp:
            return redirect('reset_password')
        else:
            messages.error(request, "Incorrect OTP.")
            return redirect('reset_verify_otp')

    return render(request, 'authsystem/reset_verify_otp.html')



def reset_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired.")
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        new_password = request.POST['password']
        user.set_password(new_password)
        user.save()
        UserOTP.objects.filter(user=user).delete()
        del request.session['reset_user_id']
        messages.success(request, "Password reset successful. Please login.")
        return redirect('login')

    return render(request, 'authsystem/reset_password.html')


from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'authsystem/dashboard.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
