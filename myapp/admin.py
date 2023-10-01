from django.contrib import admin

# Register your models here.
from .models import (Beverage, Beverage_Price, New_stock, Employee,
                      Employer, BeverageImage, Daily_Usage, Opening_stock, UserProfile, Department, ContactDetail, 
                       UserSettings, BusinessSettings)




admin.site.register(Beverage)
admin.site.register(Beverage_Price)
admin.site.register(New_stock)
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(BeverageImage)
admin.site.register(Daily_Usage)
admin.site.register(Opening_stock)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(ContactDetail)
admin.site.register(UserSettings)
admin.site.register(BusinessSettings)



admin.site.site_header = "BarManager"
admin.site.site_title = "BarManager Administration"
admin.site.index_title = "Welcome To Your Alcohol Business Management Platform"