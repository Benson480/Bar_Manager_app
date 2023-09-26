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


class Beverage(models.Model):
    name = models.CharField(max_length=255)
    Date = models.DateField(null=True,db_index=True)
    Supplier = models.CharField(max_length=255, null=True, db_index=True)
    def __str__(self):
            return f"{self.name}"

class Beverage_Price(models.Model):
    Date = models.DateField(null=True,db_index=True)
    Beverage_Product = models.ForeignKey(Beverage,on_delete=models.CASCADE, db_index=True)
    Unit_Of_Measure_Choices = (
    ("Kg", "Kg"),
    ("Ltr", "Ltr"),
    ("Bag", "Bag"),
    ("Pcs", "Pcs"),
    ("Carton", "Carton"),
    ("Pkt", "Pkt"),
    ("Tons", "Tons"),
    ("Bottles", "Bottles"),
    ("Dose", "Dose"),
    )
    Unit_Of_Measure = models.CharField(max_length=255,null=True,db_index=True,
                  choices=Unit_Of_Measure_Choices
                  )
    price_ksh = models.FloatField(blank=True, db_index=True, null=True, default=0)

    def __str__(self):
        return str(self.Beverage_Product)
    
class Opening_stock(models.Model):
    Product = models.ForeignKey(Beverage,on_delete=models.CASCADE, db_index=True)
    Stock_Take_Date = models.DateField(null=True, db_index=True, blank=True)
    Physical_balance = models.FloatField(max_length=200, db_index=True,null=True,blank=True)

    def __str__(self):
        return str(self.Product)
    
class New_stock(models.Model):
    Product = models.ForeignKey(Beverage,on_delete=models.CASCADE, db_index=True)
    Purchase_Date = models.DateField(null=True, db_index=True, blank=True)
    Purchase_Amount = models.FloatField(max_length=200, db_index=True,null=True,blank=True)

    def __str__(self):
        return str(self.Product)
    @property
    def Supplier(self):
        suppliers = Beverage.objects.all()
        for productsupplier in suppliers:
            if productsupplier.name == self.Product:
                return str(productsupplier.Supplier)
    
class Daily_Usage(models.Model):
    Product = models.ForeignKey(Beverage, on_delete=models.CASCADE, db_index=True)
    Date = models.DateField(null=True, db_index=True, blank=True)
    Place_of_use_Choices = (
        ("Internal", "Internal"),
        ("Online", "Online Sale"),
    )

    Place_of_usage = models.CharField(max_length=255, null=True, db_index=True, choices=Place_of_use_Choices)
    Used_Amount = models.FloatField(max_length=200, db_index=True, null=True, blank=True)

    @property
    def UnitOfMeasure(self):
        getUnitOfMeasure = Beverage_Price.objects.all()
        for uom in getUnitOfMeasure:
            if uom.Beverage_Product == self.Product:
                return str(uom.Unit_Of_Measure)

    @property
    def NewStock(self):
        getNewStock = New_stock.objects.all()
        for items in getNewStock:
            if items.Product == self.Product: # and self.Date >= items.Stock_Take_Date
                return str(items.Purchase_Amount)

    @property
    def Product_price(self):
        getprice = Beverage_Price.objects.all()
        for a in getprice:
            if a.Beverage_Product == self.Product:
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
        getprice = Beverage_Price.objects.all()
        for a in getprice:
            if a.Beverage_Product == self.Product:
                if self.Used_Amount is None:
                    self.Used_Amount = 0  # Convert None to zero
                DailyCost = round(a.price_ksh * self.Used_Amount, 2)
                formatted_daily_cost = '{:,.2f}'.format(DailyCost)
                return formatted_daily_cost

    @property
    def closing_stock(self):
        get_opening = Opening_stock.objects.all()
        getNewStock = New_stock.objects.all()
        getprice = Beverage_Price.objects.all()
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
        getprice = Beverage_Price.objects.all()
        for price in getprice:
            if price.Beverage_Product == self.Product:
                if self.Closing_amount is None:
                    self.closing_stock  # Calculate Closing_amount if it's not already calculated
                Closing_value = round(price.price_ksh * self.Closing_amount, 2)
                formatted_closing_value = f'{Closing_value:,.2f}'
                return formatted_closing_value



            

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

    
class Employer(models.Model):
    firstname = models.CharField(max_length=255, null=True, db_index=True)
    lastname = models.CharField(max_length=255, null=True, db_index=True)
    middlename = models.CharField(max_length=255, null=True, db_index=True)
    Business_Start_Date = models.DateField(null=True,db_index=True)
    Responsibility = models.CharField(max_length=255, null=True, db_index=True)
    def __str__(self):
            return f"{self.firstname}"
    
class BeverageImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True) # Auto generated with datetime.now()
    title = models.CharField(max_length=200, null=True, db_index=True, blank=True)
    about_Image = models.TextField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Wrap the about_Image text before saving
        if self.about_Image:
            self.about_Image = textwrap.fill(self.about_Image, width=40)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"


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


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name