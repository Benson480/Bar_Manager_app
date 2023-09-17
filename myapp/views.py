from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.template import loader
from .models import (Beverage, Beverage_Price, New_stock, Employee,
                      Employer, BeverageImage, Daily_Usage)
from django.db.models import Q
from .forms import NewUserForm
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum
import itertools
from .forms import (Beverage_Form, EmployeeForm)# DeleteFertilizerForm, Fertilizer_PricesForm, 
                    #Fertilizer_ElementsForm, Fertilizer_Form, ImageUploadForm, Fertilizer_Recycle_Form)
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import get_token
from django.contrib.auth.decorators import login_required
import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm
from django.utils import timezone
import logging
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .decorators import public_view, login_exempt
def regenerate_csrf_token(request):
    if request.method == 'GET':
        csrf_token = get_token(request)
        return HttpResponse(csrf_token)

def register_view(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            
            # Check if the username is unique
            if User.objects.filter(username=username).exists():
                signup_form.add_error('username', 'This username is already taken.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('login')  # Redirect to the desired URL after successful signup
    else:
        signup_form = SignupForm()

    return render(request, 'accounts/register.html', {'signup_form': signup_form})
    


logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            logger.warning(
                f"Login Successful at {timezone.now()} by username: {request.POST.get('username')}"
            )
            messages.success(request, f"Login Successful at {timezone.now()} by username: {request.POST.get('username')}")
            return redirect('dashboard')  # Redirect to the dashboard or desired URL
        else:
            logger.warning(
                f"Login attempt failed at {timezone.now()} by username: {request.POST.get('username')}"
            )
            messages.error(request, f"Login attempt failed at {timezone.now()} by username: {request.POST.get('username')}")

    else:
        login_form = AuthenticationForm()

    signup_form = SignupForm(request.POST)  # Pass the POST data to the signup form

    if request.method == 'POST' and signup_form.is_valid():
        username = signup_form.cleaned_data['username']
        email = signup_form.cleaned_data['email']
        password = signup_form.cleaned_data['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, f"This Username {request.POST.get('username')} is already in taken!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f"SignUp Successful at {timezone.now()} by username: {request.POST.get('username')}")
            return redirect('login')

    password_reset_form = PasswordResetForm(request.POST or None)

    if request.method == 'POST' and password_reset_form.is_valid():
        user_email = password_reset_form.cleaned_data['email']
        password_reset_form.save(
            request=request,
            from_email=None,  # Use the default email backend configured in settings
            email_template_name='accounts/password_reset.html',
        )
        messages.success(request, f"A password reset email has been sent to {user_email}.")
        return redirect('login')

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
        'password_reset_form': password_reset_form,
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "accounts/logout.html", {})  


def dashboard(request):
  template = loader.get_template('dashboard.html')
  # Update user activity in the session
  if request.user.is_authenticated:
    request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string

  return HttpResponse(template.render())


@login_required #(redirect_to='/login/')
def Employee(request):
    context ={}
 
    # create object of form
    Employee_Member = Beverage.objects.all()
    # membercost = Fertilizer_Cost.objects.all()
    # Fertilizer_list = Fertilizer.objects.all()
    # Employeeform = Fertilizer_AmountForm(request.POST or None, request.FILES or None)
    Employeeform = EmployeeForm(request.POST or None, request.FILES or None)
    
     
    # check if form data is valid
    if Employeeform.is_valid():
        # save the form data to model
        Employeeform.save()
    context = {
    'form':Employeeform,
    'Employee_Member': Employee_Member,
    # 'Fertilizer_list':Fertilizer_list,
    # 'membercost': membercost, 
    # 'fertaddform':fertaddform,
  }
    if request.user.is_authenticated:
      request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string

    return render(request, "Employee.html", context)