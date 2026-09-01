from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random
from .models import User, OtpCode
from .forms import PhoneForm, OtpForm

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    return redirect("otp_login")

def otp_login(request):
    form = PhoneForm()

    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]

            recent = OtpCode.objects.filter(
                phone=phone,
                created_at__gte = timezone.now() - timedelta(minutes=1)
            )
            if recent.exists():
                form.add_error(None, "لطفا کمی صبر کنید")
                return render(request, "accounts/otp_login.html", {"form":form})
            
            code = generate_otp()
            OtpCode.objects.create(phone=phone, code=code)

            print("OTP:", code)

            request.session["otp_phone"] = phone
            return redirect("verify_otp")
    
    return render(request, "accounts/otp_login.html", {"form": form})

def verify_otp(request):
    phone = request.session.get("otp_phone")
    if not phone:
        return redirect("otp_login")
    
    form = OtpForm()

    if request.method == "POST":
        form = OtpForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            otp = OtpCode.objects.filter(phone=phone, code=code).first()

            if otp:
                user, created = User.objects.get_or_create(
                    phone_number=phone,
                )

                login(request, user)
                otp.delete()
                request.session.flush()
                return redirect("/")
            
            form.add_error(None, "کد اشتباه یا منقضی شده")

    return render(request, "accounts/verify_otp.html", {"form":form})

def user_logout(request):
    logout(request)
    return redirect("otp_login")
            