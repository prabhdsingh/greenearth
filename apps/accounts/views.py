from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.timezone import now

from apps.accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from apps.accounts.forms import ContactForm

# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def myprofile(request):
    return render(request, 'accounts/myprofile.html', {'user': request.user})

@login_required
def user_history_view(request):
    visit_history = request.session.get('visit_history', {})
    last_visit = request.session.get('last_visit', 'Unknown')

    sorted_visits = sorted(visit_history.items(), reverse=True)

    return render(request, 'accounts/user_history.html', {
        'visit_history': sorted_visits,
        'last_visit': last_visit,
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('myprofile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect('contact_us')
    else:
        form = ContactForm()
    return render(request, 'accounts/contact_us.html', {'form': form})
