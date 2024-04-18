from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.template import loader
from .models import (Item, Item_Price, New_stock, Employee,
                      Employer, ItemImage, Daily_Usage, UserProfile, Department, UserSetting, BusinessSetting,
                      Announcement, Cart, CartItem, Order, Category, Activity)
from django.db.models import Q
from .forms import NewUserForm
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum
import itertools
from .forms import (Item_Form, EmployeeForm, Usage_Amount_Form, New_stockForm, UserProfileForm, UserSettingsForm)# DeleteFertilizerForm, Fertilizer_PricesForm, 
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
from .decorators import superuser_required
from django.contrib.auth.decorators import user_passes_test
from django.core.files import File
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.http import Http404
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from urllib.parse import urlparse
from django.urls import resolve
from .models import Student_Enrollment
from .forms import StudentForm
from .models import Career
from .forms import JobApplicationForm
from .forms import SoftwareRequestForm





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
            auth_login(request, user)
            logger.warning(
                f"Login Successful at {timezone.now()} by username: {request.POST.get('username')}"
            )
            messages.success(request, f"Login Successful at {timezone.now()} by username: {request.POST.get('username')}")
            
            # Check if there is a 'next' parameter in the URL
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('dashboard')  # Default redirect if 'next' is not provided
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


@login_required  # Add this decorator to ensure the user is authenticated
def logout_view(request):
    if request.method == "POST":
        logout(request)
        if request.user.is_authenticated:  # Check if the user is authenticated
            Activity.objects.create(user=request.user, activity_type="User Logout", user_logout=True)
        return redirect("/index/")
    return render(request, "accounts/logout.html", {})

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a UserProfile instance if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)

    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    # Check if the user has a UserProfile instance, and create one if not
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Create an Activity object to track the action
    max_activities = 50
    activities = Activity.objects.all().order_by('-timestamp')[:max_activities]
    Activity.objects.exclude(pk__in=activities).delete()

    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page after saving
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})




@login_required
def dashboard(request):
    # Retrieve or create the user_profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    max_activities = 6
    activities = Activity.objects.all().order_by('-timestamp')[:max_activities]
    Activity.objects.exclude(pk__in=activities).delete()

    # Update user activity in the session
    if request.user.is_authenticated:
        request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string

        # Get the accessed URL, excluding the login and logout URLs
        accessed_url = request.META.get('HTTP_REFERER', '')
        login_url = request.build_absolute_uri(reverse('login'))  # Replace 'login' with your login URL name
        logout_url = request.build_absolute_uri(reverse('logout'))  # Replace 'logout' with your logout URL name

        # Only save the URL if it's not a login or logout URL
        if accessed_url != login_url and accessed_url != logout_url:
            # Extract the path from the URL for a more descriptive access description
            parsed_url = urlparse(accessed_url)
            path = parsed_url.path

            # Define a mapping of paths to activity descriptions
            activity_descriptions = {
                '/Employee/': "Employee",
                '/dashboard/': "Dashboard",
                '/admin/': "Admin",
                '/Employer_dashboard/': "Employer Dashboard",
                '/Inventory/': "Inventory",
                '/profile/': "Profile",
                '/Employee_details/': "Employee Details",
                '/departments/': "Departments",
                '/report_dashboard/': "Report Dashboard",
                '/daily-usage/': "Daily Usage Report",
                '/purchased-stock/': "Purchased Stock Report",
                '/physical-stock-take/': "Physical Stock Take Report",
                '/budget/': "Budget Report",
                '/price-list/': "Price List Report",
                '/items-classification/': "Items Classification Report",
                '/forex-exchange-rates/': "Forex Exchange Rates Report",
                '/mysettings/': "Settings",
                '/business_settings/': "Business Settings",
                '/analytics/': "Analytics",
                '/dynamic_chart/': "Dynamic Chart",
                '/announcements/': "Announcements",
                '/add_to_cart/': "Add Item to Cart",
                '/purchase_item/': "Purchase Item",
                '/make_order/': "Make Order",
                '/cart_view/': "Cart View",
                '/remove_from_cart/': "Remove Item from Cart",
                '/order_confirmation/': "Order Confirmation",
                '/logout/': "User Logout",
                '/login/': "User Login",
                '/accounts/register/': "User Registration",
                '/contacts/': "Contacts",
                '/index/': "Index",
                '/about/': "About"
            }


            # Set the default description to "User accessed a page" if the path is not in the mapping
            description = activity_descriptions.get(path, "User accessed a page")

            Activity.objects.create(user=request.user, activity_type="View Access", description=description, url=accessed_url)

    context = {
        'activities': activities,
        'user_profile': user_profile,  # Add user_profile to the context dictionary
    }

    return render(request, 'dashboard.html', context)



@login_required
def report_dashboard(request):
    # Retrieve or create the user_profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Update user activity in the session
    if request.user.is_authenticated:
        request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string

    return render(request, 'reports_dashboard.html', {'user_profile': user_profile})

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def contacts(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'contacts.html', context)


def image_list(request):
    images = ItemImage.objects.all()
    return render(request, 'index.html', {'images': images})

def deleteimages(request, id):
  member = ItemImage.objects.get(id=id)
  member.delete()
  return HttpResponseRedirect(reverse("image_list"))


@login_required #(redirect_to='/login/')
def Employee_view(request):
    context ={}
 
    # create object of form
    Employee_Member = Employee.objects.all()
    # membercost = Fertilizer_Cost.objects.all()
    # Fertilizer_list = Fertilizer.objects.all()
    # Employeeform = Fertilizer_AmountForm(request.POST or None, request.FILES or None)
    Employeeform = EmployeeForm(request.POST or None, request.FILES or None)
    # Create an Activity object to track the action
    
     
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


@login_required #(redirect_to='/login/')
def Employee_details(request):
    context ={}
 
    # create object of form
    Employee_Member = Employee.objects.all()
    # membercost = Fertilizer_Cost.objects.all()
    # Fertilizer_list = Fertilizer.objects.all()
    # Employeeform = Fertilizer_AmountForm(request.POST or None, request.FILES or None)
    Employeeform = EmployeeForm(request.POST or None, request.FILES or None)
    # Create an Activity object to track the action

    
     
    # check if form data is valid
    if Employeeform.is_valid():
        # save the form data to model
        Employeeform.save()
    context = {
    'form':Employeeform,
    'Employee_Member': Employee_Member,
  }
    if request.user.is_authenticated:
      request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string

    return render(request, "EmployeeDetail.html", context)

class NotSuperUserException(Exception):
    pass

@superuser_required
@login_required
def Employer_dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a UserProfile instance if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
        

    template = loader.get_template('Employer.html')
    # Create an Activity object to track the action

    # Update user activity in the session
    if request.user.is_authenticated:
        request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string
    else:
        # Display a JavaScript alert for non-superusers
        messages.error(request, "You are not authorized to access this view.")
    
    return render(request, 'Employer.html', {'user_profile': user_profile})



@csrf_protect
@login_required #(redirect_to='/login/')
def Inventory(request):
    context ={}
 
    # create object of form
    Usage_Member = Daily_Usage.objects.all()
    New_stock_Member = New_stock.objects.all()
    Usage_form = Usage_Amount_Form(request.POST or None, request.FILES or None)
    New_stock_form = New_stockForm(request.POST or None, request.FILES or None)
    
     
    # check if form data is valid
    if Usage_form.is_valid():
        # save the form data to model
        Usage_form.save()
    context = {
    'form':Usage_form,
    'Usage_Member': Usage_Member,
    'New_stock_Member':New_stock_Member,
    # 'membercost': membercost, 
    'New_stock_form':New_stock_form,
  }
    if request.user.is_authenticated:
      request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string

    return render(request, "DailyStockUsage.html", context)


def departments(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'Departments.html', context)



# Example views
def daily_usage_report(request):
    context ={}
 
    # create object of form
    Usage_Member = Daily_Usage.objects.all()
    context = {
    'Usage_Member': Usage_Member,
  }
    if request.user.is_authenticated:
      request.session['last_activity'] = datetime.datetime.now().isoformat()  # Convert to string

    return render(request, "daily_usage_report.html", context)

def purchased_stock_report(request):
    # Implement your purchased stock report logic here
    return render(request, 'purchased_stock_report.html')

def physical_stock_take_report(request):
    # Implement your physical stock take report logic here
    return render(request, 'physical_stock_take_report.html')

def budget_report(request):
    # Implement your budget report logic here
    return render(request, 'budget_report.html')

def price_list_report(request):
    # Implement your price list report logic here
    return render(request, 'price_list_report.html')

def items_classification_report(request):
    # Implement your items classification report logic here
    return render(request, 'items_classification_report.html')

def forex_exchange_rates_report(request):
    # Implement your forex exchange rates report logic here
    return render(request, 'forex_exchange_rates_report.html')

@login_required  # Add the login_required decorator to require authentication
def mysettings(request):
    user_settings, created = UserSetting.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=user_settings)
    return render(request, 'settings.html', {'form': form})


def analytics_view(request):
    # Your data processing and graph generation code here
    # For example, create a sample graph:
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 15, 30, 25]

    plt.figure(figsize=(6, 4))
    plt.plot(x, y)
    plt.title('Sample Graph')
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')

    # Save the graph as a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the graph in base64
    graph = base64.b64encode(image_png).decode('utf-8')

    context = {'graph': graph}
    return render(request, 'analytics.html', context)

class DynamicChartView(View):
    def get(self, request, format=None):
        # Generate random data for the chart
        x = [1, 2, 3, 4, 5]
        y = [random.randint(1, 50) for _ in range(len(x))]  # Generate random y values

        chart_data = {'x': x, 'y': y}
        return render(request, 'analytics.html', {'chart_data': chart_data})


def business_settings(request):
    business_settings = BusinessSetting.objects.first()  # Retrieve the first settings object

    if request.method == 'POST':
        # Process the form data when the form is submitted
        business_settings.business_name = request.POST.get('business-name')
        business_settings.business_address = request.POST.get('business-address')
        business_settings.business_email = request.POST.get('business-email')
        business_settings.business_phone = request.POST.get('business-phone')
        business_settings.save()  # Save the updated data

    return render(request, 'business_settings.html', {'business_settings': business_settings})

def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-timestamp')
    return render(request, 'announcements.html', {'announcements': announcements})


def index(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', 'All')

    if selected_category == 'All':
        images = ItemImage.objects.all()
    else:
        category = Category.objects.get(name=selected_category)
        images = ItemImage.objects.filter(categories=category)

    categorized_images = {}
    for category in categories:
        categorized_images[category] = images.filter(categories=category)

    return render(request, 'index.html', {'categorized_images': categorized_images, 'selected_category': selected_category, 'categories': categories})

# views.py
def cart_view(request):
    # Assuming user authentication is enabled, get the current user
    user = request.user

    # Query the CartItem model to get the items in the user's cart
    cart_items = CartItem.objects.filter(cart__user=user)

    # Calculate the total price of items in the cart
    total_price = sum(item.image.price * item.quantity for item in cart_items)

    # Calculate subtotals and add them to cart_items
    for item in cart_items:
        item.subtotal = item.image.price * item.quantity

    # Query all images from the ItemImage model
    images = ItemImage.objects.all()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'images': images,
    }

    return render(request, 'cart_template.html', context)



@login_required
def add_to_cart(request, image_id):
    image = get_object_or_404(ItemImage, pk=image_id)
    user = request.user if request.user.is_authenticated else None
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, image=image)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # If the user is not authenticated, store the item details in the session
    if not user:
        item_data = {
            'image_id': image_id,
        }
        session = SessionStore(session_key=request.session.session_key)
        if 'cart_items' not in session:
            session['cart_items'] = []
        session['cart_items'].append(item_data)
        session.save()
    
    return redirect('cart_view')

def make_order(request):
    user = request.user

    # Check if the user has a cart
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        # Handle the case where the cart does not exist, e.g., by redirecting to the cart page
        return redirect('cart_view')  # You need to define this URL in your urls.py

    items_in_cart = CartItem.objects.filter(cart=cart)

    # Calculate the total price of items in the cart
    total_price = sum(item.image.price * item.quantity for item in items_in_cart)

    # Create an order and associate the selected items with it
    order = Order.objects.create(user=user, total_price=total_price)
    order.items.set(items_in_cart)

    # Retrieve the associated images
    ordered_images = [item.image for item in items_in_cart]

    # Clear the cart and redirect to the order confirmation view
    cart.delete()
    
    # Pass the ordered_images to the order_confirmation_view
    return HttpResponseRedirect(reverse('order_confirmation_view', args=(order.id,)) + f"?ordered_images={','.join([str(image.id) for image in ordered_images])}")





def order_confirmation_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")

    ordered_images = request.GET.get('ordered_images', '').split(',')
    ordered_images_objects = [get_object_or_404(ItemImage, id=image_id) for image_id in ordered_images]

    context = {
        'order': order,
        'ordered_images': ordered_images_objects,
    }
    return render(request, 'order_confirmation.html', context)



def purchase_item(request, image_id):
    # Implement the logic to handle a purchase (e.g., deduct from user's balance)
    return redirect('success_view')  # Redirect to a success view


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    return redirect('cart_view')

def success_page(request):
    return render(request, 'success_page.html')

def enroll_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')   # Redirect to a success page or URL
        else:
            # Handle invalid form submission
            # Check if the error is due to duplicate email
            if 'email' in form.errors:
                messages.error(request, "Student enrollment with this Email already exists.")
            return render(request, 'enroll_student.html', {'form': form})
    else:
        # If the request method is not POST, render the form
        form = StudentForm()

    # If form is not valid or it's a GET request, render the form with errors or empty form
    return render(request, 'enroll_student.html', {'form': form})


def career_detail(request, pk):
    career = Career.objects.get(pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.career = career
            job_application.save()
            messages.success(request, 'Your job application has been submitted successfully.')
            return redirect('career_detail', pk=pk)
    else:
        form = JobApplicationForm()
    return render(request, 'career_detail.html', {'career': career, 'form': form})

def careers_list(request):
    careers = Career.objects.all().order_by('-published_date')
    return render(request, 'careers_list.html', {'careers': careers})

def request_software(request):
    if request.method == 'POST':
        form = SoftwareRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('request_success')  # Redirect to a success page
    else:
        form = SoftwareRequestForm()
    return render(request, 'request_software.html', {'form': form})

def request_success(request):
    return render(request, 'request_success.html')