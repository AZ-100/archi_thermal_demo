from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.register(CarouselImage)
admin.site.register(AboutUsSection)
admin.site.register(WindowSection)
admin.site.register(DoorSection)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(DoorWindow)
admin.site.register(Event)
admin.site.register(UserIPLog)
@admin.register(Product) #manage this model vs the admin dashboard
class ProductAdmin(admin.ModelAdmin):#controls how model is showed/displayed
    list_display = ('name', 'product_type')#columns that will be showed in interface
    list_filter = ('product_type', 'is_available')#filter tags 
    ordering = ['name'] #how to order them(by name)
    
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'requested_date') #fields that will be displayed 
    search_fields = ('name', 'product__name') #can search using customer name or product name 
    date_hierarchy = 'requested_date'  #date filter 
    ordering = ['-requested_date'] #orders by requested date

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_date')#view for in admin dashboard
    search_fields = ('name', 'email')#what fields can you search up
    date_hierarchy = 'sent_date' #date filter 
    ordering = ['-sent_date'] #- means descending order (newest to oldest records are shown)

