from django.db import models
#allows to dynamically change index page content
from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='gallery/')


class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    caption = models.CharField(max_length=255)

class AboutUsSection(models.Model):
    image = models.ImageField(upload_to='about_us_images/')
    text = models.TextField()

class WindowSection(models.Model):
    image = models.ImageField(upload_to='window_images/')
    heading = models.CharField(max_length=100)
    text = models.TextField()

class DoorSection(models.Model):
    image = models.ImageField(upload_to='door_images/')
    heading = models.CharField(max_length=100)
    text = models.TextField()

# Product Model for Windows and Doors (Base Class)
class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('window', 'Window'),
        ('door', 'Door'),
        ('window_door_installation','Window Door Installation'),
        ('curtain_walling','Curtain Walling'),
        ('office_fit_out','Office Fit Out'),
    ]
    
    name = models.CharField(max_length=100, help_text="Name of the product")
    description = models.TextField(help_text="Description of the product")
    image = models.ImageField(upload_to='products/', help_text="Upload an image of the product")
    product_type = models.CharField(max_length=100, choices=PRODUCT_TYPE_CHOICES, help_text="Specify if it is a window or door")

    # Admin-only fields (not visible to users)
    is_available = models.BooleanField(default=True, help_text="Product availability status")


    def __str__(self): #how to return the model. 
        return self.name
    

class DoorWindow(Product): #inherits from base model 
    model_number = models.CharField(max_length=50, help_text="Model number of the window")

    feature1 =models.CharField(max_length=200)
    feature2 =models.CharField(max_length=200)
    feature3 =models.CharField(max_length=200)

    application = models.CharField(max_length=200)

    # Performance Specifications
    u_value = models.DecimalField(max_digits=4, decimal_places=2, default=0.25, help_text="Thermal performance (U-Value)",null=True,blank=True)
    sound_transmission_class = models.IntegerField(default=45, help_text="Sound insulation rating (STC)",null=True,blank=True)

    # Technical Specifications
    certifications = models.CharField(max_length=255, default="Energy Star, LEED Compliant", help_text="Certifications and compliances",null=True,blank=True)

    profile_wall_thickness = models.DecimalField(max_digits=3, decimal_places=1, default=1.8, help_text="Profile wall thickness in mm",null=True,blank=True)
    profile_grade = models.CharField(max_length=10, default='6063-T5', help_text="Profile grade",null=True,blank=True)
    insulation_strip_width = models.DecimalField(max_digits=4, decimal_places=1, default=14.8, help_text="Insulation strip width in mm",null=True,blank=True)
    opening_method = models.CharField(max_length=100, default='Inward opening, inward tilting', help_text="Method of opening",null=True,blank=True)
    hardware_configuration = models.CharField(max_length=100, default='HOPPE, G-U', help_text="Hardware configuration",null=True,blank=True)
    opening_leaf_size_range = models.CharField(max_length=100, default='Width 500–1200 mm, Height 500–2800 mm', help_text="Range of opening leaf sizes",null=True,blank=True)
    glass_holding_thickness = models.CharField(max_length=50, default='25–54 mm', help_text="Glass holding thickness range",null=True,blank=True)
    air_tightness = models.IntegerField(default=8, help_text="Air tightness grade",null=True,blank=True)
    water_tightness = models.IntegerField(default=6, help_text="Water tightness grade",null=True,blank=True)
    wind_pressure_resistance = models.IntegerField(default=9, help_text="Wind pressure resistance grade",null=True,blank=True)
    sound_insulation = models.CharField(max_length=50, default='Up to 45 dB', help_text="Sound insulation rating",null=True,blank=True)
    burglary_resistance = models.CharField(max_length=50, default='Up to RC2', help_text="Burglary resistance rating",null=True,blank=True)
    regular_colors = models.CharField(max_length=255, default='Titanium Grey, Amber Brown, Jazz White', help_text="Regular colors",null=True,blank=True)
    optional_colors = models.CharField(max_length=255, blank=True, help_text="Optional colors",null=True)

    # Additional Images
    additional_image_1 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="First additional product image")
    additional_image_2 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Second additional product image")

    def __str__(self):
        return f"Window: {self.name}"
    
  


# Quote Request Model for users to request custom quotes
class QuoteRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #if product is deleted, quote would be as well
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    suburb = models.CharField(max_length=150)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # New field for IP address
    job_type = models.CharField(max_length=50, choices=[
        ('new_build', 'New Build'),
        ('replacements', 'Replacements'),
        ('extensions', 'Extensions'),
        ('curtain_walling', 'Curtain Walling'),
        ('commercial', 'Commercial'),
        ('not_sure', 'Not Sure'),
    ])
    requested_date = models.DateTimeField(auto_now_add=True)#   automatically sets the current time 

    def __str__(self):
        return f"Quote Request by {self.name} for {self.product.name}" #dispaly name on the django interface
        #the product self.product.name is from the product model

# Contact Form Model for handling customer inquiries
class Contact(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True,)
    message = models.TextField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # New field for IP address
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
    )
    customer = models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    # quantity = models.CharField(max_length=100)
    status=models.CharField(max_length=200, null=True,choices=STATUS)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.title

    @property
    def formatted_date(self): #return this date of month
        return self.date.strftime('%d')

    @property
    def formatted_month(self): #return month abbreviation 
        return self.date.strftime('%b')
    
class UserIPLog(models.Model):
    ip_address = models.GenericIPAddressField()
    visit_time = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    page_visited = models.CharField(max_length=255, null=True, blank=True)  # Ensure this line exists
    time_now = models.DateTimeField()
    region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.ip_address} from {self.city}, {self.region}, {self.country}"