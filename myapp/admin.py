from django.contrib import admin

# Register your models here.
from .models import (Item, Item_Price, New_stock, Employee,
                      Employer, ItemImage, Daily_Usage, Opening_stock, UserProfile, Department, ContactDetail, 
                       UserSetting, BusinessSetting, Announcement, Category, Student_Enrollment)



admin.site.register(Item)
admin.site.register(Item_Price)
admin.site.register(New_stock)
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(ItemImage)
admin.site.register(Daily_Usage)
admin.site.register(Opening_stock)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(ContactDetail)
admin.site.register(UserSetting)
admin.site.register(BusinessSetting)
admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Student_Enrollment)



admin.site.site_header = "Bentha Technologies"
admin.site.site_title = "Bentha Technologies Administration"
admin.site.index_title = "Welcome To Your Bentha Technologies Management Platform"