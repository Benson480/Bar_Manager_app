from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (Item, Item_Price, New_stock, Employee,
                      Employer, ItemImage, Daily_Usage, UserSetting)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from .models import Student_Enrollment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'profile_picture', 'bio', 'location', 'website', 'date_of_birth']
# Create your forms here.
class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

class LoginForm(AuthenticationForm):
    # currently Not in use -- Hard to implement
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	

class DateInput(forms.DateInput):
    input_type = 'date'


class Item_Form(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Item
		fields = ['Date', 'name', 'Supplier']
		widgets = {
			'Date': DateInput(),
			
		}

class Item_PriceForm(forms.ModelForm):
	# specifIed the name of model to use
	price_ksh = forms.DecimalField(required=True,label= "Price_Ksh", widget=forms.NumberInput(attrs={'placeholder': 0}))
	class Meta:
		model = Item_Price
		fields = ['Date', 'Item_Product','Unit_Of_Measure', 'price_ksh']
		widgets = {
			'Date': DateInput(),
			
		}

class New_stockForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = New_stock
		fields = ['Purchase_Date','Product', 'Purchase_Amount']
		widgets = {
			'Purchase_Date': DateInput(),
			
		}               


class Usage_Amount_Form(forms.ModelForm):
    # Date = forms.DateField(input_formats=['%d-%m-%Y'])
    Observation = forms.CharField(
        required=False,
        label="Observation",
        widget=forms.Textarea(attrs={'placeholder': "", 'rows': 3, 'cols': 40}))
    Used_Amount = forms.DecimalField(required=True,label= "Product Amount", widget=forms.NumberInput(attrs={'placeholder': 0}))
    class Meta:
        model = Daily_Usage
        fields = ['Date', 'Product', 'Place_of_usage', 'Used_Amount', 'Observation']
        widgets = {
            'Date': DateInput(),
	    
        }

class EmployeeForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Employee
		fields = ['Payroll_number', 'Last_date_attendance', 'firstname','lastname', 'middlename', 'Date_employed','Performance', 'Basic_Salary', 'Allowances', 'Designation']
		widgets = {
			'Date_employed': DateInput(),
			
		}       


class EmployerForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Employer
		fields = ['firstname','lastname', 'middlename', 'Business_Start_Date', 'Responsibility']
		widgets = {
			'Business_Start_Date': DateInput(),
			
		}       


	
class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image', 'about_Image', 'title']
		
		
class DeleteItemForm(forms.ModelForm): #This can be handled using JavaScript
    class Meta:
        model = Item
        fields = []
		
class DeleteEmployeeForm(forms.ModelForm): #This can be handled using JavaScript
    class Meta:
        model = Employee

        fields = []
        
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSetting
        fields = ['dark_mode', 'notifications', 'font_size']
        

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student_Enrollment
        fields = '__all__'