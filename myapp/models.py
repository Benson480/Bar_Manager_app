from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.functions import Coalesce
from django.template.defaultfilters import wordwrap
import textwrap
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files import File
# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=255)
    Date = models.DateField(null=True,db_index=True)
    Supplier = models.CharField(max_length=255, null=True, db_index=True)
    def __str__(self):
            return f"{self.name}"

class Item_Price(models.Model):
    Date = models.DateField(null=True,db_index=True)
    Item_Product = models.ForeignKey(Item,on_delete=models.CASCADE, db_index=True)
    Unit_Of_Measure_Choices = (
    ("Kg", "Kg"),
    ("Ltr", "Ltr"),
    ("Bag", "Bag"),
    ("Pcs", "Pcs"),
    ("Pcs", "Pc"),
    ("Carton", "Carton"),
    ("Pkt", "Pkt"),
    ("Tons", "Tons"),
    ("Bottles", "Bottles"),
    ("Dose", "Dose"),
    ("Course", "Course"),
    ("Square Meter", "Square Meter"),
    ("Case", "Case"),
    ("Custom Software", "Custom Software"),
    )
    Unit_Of_Measure = models.CharField(max_length=255,null=True,db_index=True,
                  choices=Unit_Of_Measure_Choices
                  )
    price_ksh = models.FloatField(blank=True, db_index=True, null=True, default=0)
    Price_Negotiable = models.CharField(max_length=255, null=True, db_index=True)


    def __str__(self):
        return str(self.Item_Product)
    
class Opening_stock(models.Model):
    Product = models.ForeignKey(Item,on_delete=models.CASCADE, db_index=True)
    Stock_Take_Date = models.DateField(null=True, db_index=True, blank=True)
    Physical_balance = models.FloatField(max_length=200, db_index=True,null=True,blank=True)

    def __str__(self):
        return str(self.Product)
    
class New_stock(models.Model):
    Product = models.ForeignKey(Item,on_delete=models.CASCADE, db_index=True)
    Purchase_Date = models.DateField(null=True, db_index=True, blank=True)
    Purchase_Amount = models.FloatField(max_length=200, db_index=True,null=True,blank=True)


    def __str__(self):
        return str(self.Product)
    @property
    def Supplier(self):
        suppliers = Item.objects.all()
        for productsupplier in suppliers:
            if productsupplier.name == self.Product:
                return str(productsupplier.Supplier)
    
class Daily_Usage(models.Model):
    Product = models.ForeignKey(Item, on_delete=models.CASCADE, db_index=True)
    Date = models.DateField(null=True, db_index=True, blank=True)
    Place_of_use_Choices = (
        ("Internal Sales", "Internal Sales"),
        ("Online Sale", "Online Sale"),
    )

    Place_of_usage = models.CharField(max_length=255, null=True, db_index=True, choices=Place_of_use_Choices)
    Used_Amount = models.FloatField(max_length=200, db_index=True, null=True, blank=True)

    def __str__(self):
        return f"{self.Date} {self.Product} {self.Place_of_usage}"


    @property
    def UnitOfMeasure(self):
        getUnitOfMeasure = Item_Price.objects.all()
        for uom in getUnitOfMeasure:
            if uom.Item_Product == self.Product:
                return str(uom.Unit_Of_Measure)

    @property
    def NewStock(self):
        getNewStock = New_stock.objects.all()
        for items in getNewStock:
            if items.Product == self.Product: # and self.Date >= items.Stock_Take_Date
                return str(items.Purchase_Amount)

    @property
    def Product_price(self):
        getprice = Item_Price.objects.all()
        for a in getprice:
            if a.Item_Product == self.Product:
                price = round(a.price_ksh, 2)
                formatted_price = "{:,.2f}".format(price)
                return formatted_price

    @property
    def Opening_stock_data(self):
        getnew = Opening_stock.objects.all()
        for items in getnew:
            if items.Product == self.Product:
                Physical_stock = round(items.Physical_balance, 2)
                formatted_physical_stock = "{:,.2f}".format(Physical_stock)
                return formatted_physical_stock

    @property
    def Daily_cost(self):
        getprice = Item_Price.objects.all()
        for a in getprice:
            if a.Item_Product == self.Product:
                if self.Used_Amount is None:
                    self.Used_Amount = 0  # Convert None to zero
                DailyCost = round(a.price_ksh * self.Used_Amount, 2)
                formatted_daily_cost = '{:,.2f}'.format(DailyCost)
                return formatted_daily_cost

    @property
    def closing_stock(self):
        get_opening = Opening_stock.objects.all()
        getNewStock = New_stock.objects.all()
        getprice = Item_Price.objects.all()
        for opening in get_opening:
            if opening.Product == self.Product:
                Physical_stock = round(opening.Physical_balance, 2)
        for new in getNewStock:
            if new.Product == self.Product:
                Purchase_Amount = round(new.Purchase_Amount, 2)
                if self.Used_Amount is None:
                    self.Used_Amount = 0  # Convert None to zero
                if Physical_stock is None:
                    Physical_stock = 0  # Convert None to zero
                self.Closing_amount = round((Physical_stock + Purchase_Amount) - self.Used_Amount, 2)
                return '{:,.2f}'.format(self.Closing_amount)

    @property
    def closing_stock_value(self):
        getprice = Item_Price.objects.all()
        for price in getprice:
            if price.Item_Product == self.Product:
                if self.Closing_amount is None:
                    self.closing_stock  # Calculate Closing_amount if it's not already calculated
                Closing_value = round(price.price_ksh * self.Closing_amount, 2)
                formatted_closing_value = f'{Closing_value:,.2f}'
                return formatted_closing_value

    @property
    def Daily_usage_cost(self):
        getprice = Item_Price.objects.all()
        for price in getprice:
            if price.Item_Product == self.Product:
                if self.Used_Amount is None:
                    self.Used_Amount  # Calculate Closing_amount if it's not already calculated
                Daily_used_cost = round(price.price_ksh * self.Used_Amount, 2)
                Formatted_used_cost = f'{Daily_used_cost:,.2f}'
                return Formatted_used_cost

            

class Employee(models.Model):
    Payroll_number = models.CharField(max_length=255, null=True, db_index=True)
    firstname = models.CharField(max_length=255, null=True, db_index=True)
    middlename = models.CharField(max_length=255, null=True, db_index=True)
    lastname = models.CharField(max_length=255, null=True, db_index=True)
    Date_employed = models.DateField(null=True,db_index=True)
    Last_date_attendance = models.DateField(null=True,db_index=True)
    Basic_Salary = models.FloatField(max_length=255, null=True, db_index=True)
    Allowances = models.FloatField(max_length=255, null=True, db_index=True)
    Designation = models.CharField(max_length=255, null=True, db_index=True)
    Performance_Choices = (
    ("Great", "Great"),
    ("Better", "Better"),
    ("Worse", "Worse"),
    ("Other", "Other. Please specify"),
    )
    Performance = models.CharField(max_length=255,null=True,db_index=True,
                  choices=Performance_Choices
                  )
    
    def __str__(self):
            return f"{self.Payroll_number} {self.firstname} {self.middlename} {self.Designation}"
    
    @property
    def Gross_pay(self):
        grosspay = round(self.Basic_Salary + self.Allowances, 2)
        formatted_grosspay = '{:,.2f}'.format(grosspay)
        return formatted_grosspay
    
    @property
    def Basic_pay(self):
        Basic_payed = round(self.Basic_Salary, 2)
        formatted_Basic_pay = '{:,.2f}'.format(Basic_payed)
        return formatted_Basic_pay
    
    @property
    def Allowances_pay(self):
        Allowances_payed = round(self.Allowances, 2)
        formatted_Allowances = '{:,.2f}'.format(Allowances_payed)
        return formatted_Allowances

    
class Employer(models.Model):
    firstname = models.CharField(max_length=255, null=True, db_index=True)
    lastname = models.CharField(max_length=255, null=True, db_index=True)
    middlename = models.CharField(max_length=255, null=True, db_index=True)
    Business_Start_Date = models.DateField(null=True,db_index=True)
    Responsibility = models.CharField(max_length=255, null=True, db_index=True)
    def __str__(self):
            return f"{self.firstname}"

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class ItemImage(models.Model):
    Product = models.ForeignKey(Item,on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='images', blank=True)
    Date = models.DateField(null=True, db_index=True, blank=True)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True) # Auto generated with datetime.now()
    title = models.CharField(max_length=200, null=True, db_index=True, blank=True)
    about_Image = models.TextField(max_length=2000, null=True, blank=True)
    
    def availability_description(self):
        if self.Date:
            return f"Available in {self.Date.strftime('%B %d, %Y')}"
        else:
            return "Availability not specified"
    Status_Choices = (
    ("default", "Select availability..."),
    ("available", "Available now"),
    ("Service available", " Service Available now"),
    ("Out of Stock", "Out of Stock"),
    ("future", availability_description),
    )

    status = models.CharField(max_length=255,null=True,db_index=True,
                  choices=Status_Choices
                  )

    def save(self, *args, **kwargs):
        # Wrap the about_Image text before saving
        if self.about_Image:
            self.about_Image = textwrap.fill(self.about_Image, width=40)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Product} Image uploaded at {self.uploaded_at}"
    
    
    @property
    def UnitOfMeasure(self):
        getUnitOfMeasure = Item_Price.objects.all()
        for uom in getUnitOfMeasure:
            if uom.Item_Product == self.Product:
                return str(uom.Unit_Of_Measure)
            
    @property
    def price(self):
        getprice = Item_Price.objects.all()
        for a in getprice:
            if a.Item_Product == self.Product:
                Price = round(a.price_ksh, 2)
                formatted_price = "{:,.2f}".format(Price)
                # Remove commas from the formatted price string and then convert to float
                formatted_price = formatted_price.replace(',', '')
                return float(formatted_price)

        # If no matching price is found, return 0.0 as a float
        return 0.0





class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other fields you need

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    image = models.ForeignKey(ItemImage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Add any other fields you need

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    Item_image = models.ForeignKey(ItemImage, on_delete=models.CASCADE, null=True)  # Establish the relationship
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(CartItem)  # Link Order to CartItems
    # Add any other fields you need

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add fields for user profile details like name, picture, etc.
    full_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Create the UserProfile instance when a new User is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Save the UserProfile instance when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Create a UserProfile instance if it doesn't exist
        UserProfile.objects.create(user=instance)



class ContactDetail(models.Model):
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Contact Details {self.email} {self.phone} {self.address}"

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    contact_details = models.OneToOneField(ContactDetail, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name


class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    notifications = models.BooleanField(default=True)
    font_size = models.CharField(max_length=20, default='medium')

    def __str__(self):
        return self.user.username + "'s Settings"
    
class BusinessSetting(models.Model):
    business_name = models.CharField(max_length=100)
    business_address = models.TextField()
    business_email = models.EmailField()
    business_phone = models.CharField(max_length=30)

    def __str__(self):
        return self.business_name
    
from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=[
        ('news', 'News'),
        ('advertisement', 'Advertisement'),
        ('video', 'Video Upload'),
    ])
    image = models.ImageField(upload_to='announcement_images/', blank=True, null=True)
    image_description = models.CharField(max_length=255, blank=True, null=True, help_text="Description of the image")
    video_url = models.URLField(blank=True, null=True)
    countdown_to = models.DateTimeField(blank=True, null=True)
    venue = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    user_logout = models.BooleanField(default=False)
    url = models.CharField(max_length=255, blank=True, null=True)  # Add a URL field

    def __str__(self):
        return f'{self.user} - {self.activity_type} - {self.timestamp}'


#Student enrollment in the course model
class Student_Enrollment(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField()
    previous_school = models.CharField(max_length=100)
    year_of_study = models.IntegerField()
    date_enrolled = models.DateField(auto_now_add=True)
    Do_you_have_smartphone_or_computer = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Career(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    career = models.ForeignKey(Career, on_delete=models.CASCADE)

    def __str__(self):
        return f"Application for {self.career.title} by {self.full_name}"
    

class SoftwareRequest(models.Model):
    CUSTOMER_TYPE_CHOICES = (
        ('Individual', 'Individual'),
        ('Small Business', 'Small Business'),
        ('Enterprise', 'Enterprise'),
    )
    SOFTWARE_TYPE_CHOICES = (
        ('Mobile Application', 'Mobile Application'),
        ('Website', 'Website'),
        ('Desktop Application', 'Desktop Application'),
        ('Other', 'Other'),
    )

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    budget_in_Ksh = models.DecimalField(max_digits=10, decimal_places=2)
    target_customers = models.TextField()
    software_type = models.CharField(max_length=50, choices=SOFTWARE_TYPE_CHOICES)
    additional_specifications = models.TextField(blank=True)
    customer_type = models.CharField(max_length=50, choices=CUSTOMER_TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.software_type}"