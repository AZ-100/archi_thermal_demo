import ipinfo
from .models import UserIPLog
from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import *
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
# Create your views here.
from .filters import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import now, timedelta
def get_client_ip(request):
    # Retrieve the 'HTTP_X_FORWARDED_FOR' header from the request's META information
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    # Check if the header exists (indicating a proxy may be used)
    if x_forwarded_for:
        # Split the header by commas and take the first IP address
        ip = x_forwarded_for.split(',')[0]
    else:
        # If the header does not exist, fall back to the remote address of the request
        ip = request.META.get('REMOTE_ADDR')
    
    # Return the extracted IP address
    return ip

handler = ipinfo.getHandler(settings.IPINFO_ACCESS_TOKEN)

@login_required(login_url='login')
def record_user_ip(request):
    user_ip = get_client_ip(request)
    details = handler.getDetails(user_ip)

    # Get location details with fallbacks
    city = getattr(details, 'city', 'Unknown')
    region = getattr(details, 'region', 'Unknown')
    country = getattr(details, 'country', 'Unknown')

    time_now = datetime.now()  # Replace this if you have a specific time variable
    
    UserIPLog.objects.create(
        ip_address=user_ip,
        city=city,
        region=region,
        country=country,
        user_agent=request.META.get('HTTP_USER_AGENT', 'unknown'),
        page_visited=request.path,  # Ensure this matches the model field
        time_now=time_now  # Use your time variable here

    )

def index(request):
    carousel_images = CarouselImage.objects.all()
    about_us_sections = AboutUsSection.objects.all()
    window_sections = WindowSection.objects.all()
    door_sections = DoorSection.objects.all()
    current_year = timezone.now().year
    events = Event.objects.all().order_by('date')
    record_user_ip(request)  # Log the user's IP
    doors = Product.objects.filter(product_type='door')  # Get all door products
    windows = Product.objects.filter(product_type='window')  # Get all window products
    context = {
        'carousel_images': carousel_images,
        'about_us_sections': about_us_sections,
        'window_sections': window_sections,
        'door_sections': door_sections,
        'current_year': current_year,
        'events':events,
         'products_by_type': {
            'door': doors,
            'window': windows,
        }
    }
    
    return render(request, 'windows/index.html', context)
def navbar_page(request):
    products = Product.objects.all()
    print(products)
    # Add any additional filtering if needed
    # For example, if you want to include other product types:
    window_door_installations = Product.objects.filter(product_type='window door installation')
    curtain_walling = Product.objects.filter(product_type='curtain walling')
    office_fit_out = Product.objects.filter(product_type='office fit out')

    context = {'window_door_installations':window_door_installations, "curtain_walling":curtain_walling, "office_fit_out":office_fit_out,"products":products}
    return render(request, 'navbar.html',context)
    

def register_page(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard')  # Specify a URL or view name to redirect to
        else:
            raise PermissionDenied
    form = CreateUserForm()  # Initialize the form

    if request.method == "POST":
        form = CreateUserForm(request.POST)  # Get data from POST
        if form.is_valid():  # Call is_valid() method correctly
            form.save()  # Save the user
            user = form.cleaned_data.get('username')  # Get the username
            messages.success(request, "Account was created for {}".format(user))            
            return redirect('login')
        else:
            print(form.errors)  # Print errors for debugging
            messages.error(request, 'Please correct the errors below.')
    
    context = {'form': form}  # Use the form with errors if present
    return render(request, 'windows/register.html', context)


def login_page(request):
    record_user_ip(request)  # Log the user's IP
    if request.method == "POST":
        username = request.POST.get('username')  # Use parentheses instead of brackets
        password = request.POST.get('password')  # Use parentheses instead of brackets

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff or request.user.is_superuser:
                return redirect('dashboard')  # Specify a URL or view name to redirect to
            else:
                raise PermissionDenied
        else:
            messages.info(request, "Username OR password is incorrect")
            return render(request, 'windows/login.html')  # Return to the login page with the message
    
    if request.user.is_authenticated:
        return redirect('dashboard')  # Specify a URL or view name to redirect to

    return render(request, 'windows/login.html')  # Render the login page for GET requests


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def admin_dashboard(request):
    products = Product.objects.all()
    quote_requests = QuoteRequest.objects.all()
    contacts = Contact.objects.all()
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered= orders.filter(status='Delivered').count()
    pending= orders.filter(status='Pending').count()
    
    context = {
        'products': products,
        'quote_requests': quote_requests,
        'contacts': contacts,
        'customers':customers,
        'orders':orders,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delieverd':delivered,
        'pending':pending,
    
    }
    return render(request, 'windows/dashboard.html', context)



# View for displaying Products
def about_page(request):
    record_user_ip(request)  # Log the user's IP
    # Manually set the video URL
    video_url = settings.MEDIA_URL + 'videos/features.mp4'  # Adjust the path as necessary

    return render(request, 'windows/about.html', {
        'video_url': video_url  # Pass the video URL to the template
    })



def product_list(request):
    record_user_ip(request)  # Log the user's IP
    products = Product.objects.all()
    return render(request, 'windows/product_list.html', {'products': products})

# View for handling Quote Requests
# def request_quote(request):
#     form = QuoteForm()

#     title = 'Request Quote'
#     if request.method == "POST":#checks if someone is submitting the data 
#         form = QuoteForm(request.POST) #create instance with filled data
#         if form.is_valid(): #check if is valid 
#             form.save()#saves 
#             messages.success(request, "Quote Request submitted successfully!")
#             return redirect('thanks')
#     context = {'form':form, 'title':title}
#     return render(request, 'windows/form.html', context)


def request_quote(request):
    # Create a new instance of the QuoteForm for the initial GET request
    form = QuoteForm()
    
    # Set the title for the template
    title = 'Request Quote'
    
    # Call the function to get the client's IP address
    user_ip = get_client_ip(request)
    
    # Output the user's IP address to the console for debugging
    print(f"User IP Address: {user_ip}")

    # Check if the request method is POST (indicating form submission)
    if request.method == "POST":
        # Create a new instance of the QuoteForm with the submitted data
        form = QuoteForm(request.POST)

        record_user_ip(request)  # Log the user's IP
        
        # Validate the form data
        if form.is_valid():
            # Create a quote request object without saving it to the database yet
            quote_request = form.save(commit=False)
            
            # Store the user's IP address in the quote request object
            quote_request.ip_address = user_ip
            
            # Save the quote request object to the database
            quote_request.save()

                  
            # Prepare the email
            subject = "New Quote Request"
            message = f"Quote Request Details:\n\n{form.cleaned_data}"
            from_email = 'info@archithermal.com.au'  # Sender email
            recipient_list = ['john@archithermal.com.au']  # Replace with your email
            
            # Send the email
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "Quote Request submitted successfully!")
            
            # Add a success message to be displayed to the user
            messages.success(request, "Quote Request submitted successfully!")
            
            # Redirect the user to a 'thank you' page after successful submission
            return redirect('thanks')

    # Prepare the context dictionary with the form and title to render the template
    context = {'form': form, 'title': title}
    
    # Render the form template with the provided context
    return render(request, 'windows/quote.html', context)



# View for handling Contact Form submissions
def contact(request):
    form = ContactForm()
    title = 'Contact Us'

    if request.method == "POST":
        form = ContactForm(request.POST)
        record_user_ip(request)  # Log the user's IP
        if form.is_valid():
            form.save()
            messages.success(request, "Contact Form submitted successfully!")
            return redirect('thanks')
    context = {'form':form, 'title':title}
    return render(request, 'windows/contact.html', context)


def thanks(request):
    return render(request, 'windows/thanks.html')

@login_required(login_url='login')
def product_update(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    
    title = 'Update Project'

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect('dashboard')
    context = {'form':form, 'title':title}
    return render(request, 'windows/form.html', context)

@login_required(login_url='login')
def window_update(request, pk):
    # Get the specific Window instance
    window = get_object_or_404(DoorWindow, id=pk)
    
    # Use the WindowForm with the instance of Window
    form = WindowForm(instance=window)
    
    title = 'Update Window'

    if request.method == "POST":
        form = WindowForm(request.POST, instance=window)
        if form.is_valid():
            form.save()
            messages.success(request, "Window Updated Successfully")
            return redirect('dashboard')
    
    context = {'form': form, 'title': title}
    return render(request, 'windows/form.html', context)


@login_required(login_url='login')
def product_create(request):
    form = ProductForm()
    x = None
    title = 'Create Project'

    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sucessfully Created")
            return redirect('dashboard')
        else:
            x = form.errors
    context = {'form':form, 'title':title,'x':x,}
    return render(request, 'windows/form.html', context)
    
@login_required(login_url='login')
def product_delete(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('dashboard')
    context = {'object':product}
    return render(request, 'windows/delete_template.html', context)

@login_required(login_url='login')
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer}) #in quotes represent field that wants to be prefilled and other is the model
    order = Order.objects.all()

    title = 'Create Order'

    if request.method == "POST":
        form = OrderForm(request.POST) #retrieves data clients put in
        if form.is_valid:
            form.save()
            messages.success(request, "Sucessfully Created")
            return redirect('dashboard')
    context = {'form':form, 'title':title}
    return render(request, 'windows/form.html', context)


@login_required(login_url='login')
def update_order(request,pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)

    title = 'Update Order'

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order) #retrieves data clients put in
        if form.is_valid:  #item instance is order
            form.save()
            messages.success(request, "Sucessfully Created")
            return redirect('dashboard')
    context = {'form':form, 'title':title}
    return render(request, 'windows/form.html', context)
    
@login_required(login_url='login')
def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('dashboard')
    context = {'object':order}
    return render(request, 'windows/delete_template.html', context)

@login_required(login_url='login')
def create_customer(request):
    form = CustomerForm()
    order = Order.objects.all()

    title = 'New Customer'

    if request.method == "POST":
        form = CustomerForm(request.POST) #retrieves data clients put in
        if form.is_valid:
            form.save()
            messages.success(request, "Sucessfully Created")
            return redirect('dashboard')
    context = {'form':form, 'title':title}
    return render(request, 'windows/form.html', context)

def customer_page(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    context = {'customers':customers,
                'orders':orders,
                'order_count':order_count,
                'myfilter':myfilter}
    return render(request,'windows/customer.html',context)


@login_required(login_url='login')
def update_customer(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    
    title = 'Update Customer'

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect('dashboard')
    context = {'form':form, 'title':title}
    return render(request, 'windows/form.html', context)

def gallery(request):
    images = Image.objects.all()
    return render(request, 'windows/gallery.html', {'images': images})

@login_required(login_url='login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = ImageUploadForm()
    return render(request, 'windows/upload.html', {'form': form})


def services(request):
    record_user_ip(request)  # Log the user's IP
      # Manually set the video URL
    video_url = settings.MEDIA_URL + 'videos/features.mp4'  # Adjust the path as necessary

    return render(request, 'windows/services.html',{ 'video_url': video_url })

def careers(request):
    return render(request, 'windows/careers.html')

def window_list(request):
    # product = get_object_or_404(Product, product_type='window')
    
    # # Get related products, excluding the current one
    # related_products = Product.objects.filter(product_type='window')
    
    # context = {
    #     'product': product,
    #     'related_products': related_products,
    # }
    
    return render(request, 'windows/product_list.html')

def product_detail(request, pk):
    record_user_ip(request)  # Log the user's IP
    """ View for a specific product detail page """
    product = get_object_or_404(DoorWindow, pk=pk)
    return render(request, 'windows/product_detail.html', {'product': product})

def doors_list(request):
    record_user_ip(request)  # Log the user's IP
    return render(request, 'windows/doors.html')

def privacy(request):
    record_user_ip(request)  # Log the user's IP
    return render(request, 'windows/privacy.html')

def terms(request):
    record_user_ip(request)  # Log the user's IP
    return render(request, 'windows/terms.html')
def codeconduct(request):
    record_user_ip(request)  # Log the user's IP
    return render(request, 'windows/code-conduct.html')
def wechat(request):
    return render(request, 'windows/wechat.html')
def events(request):
    record_user_ip(request)  # Log the user's IP
    events = Event.objects.all().order_by('date')
    context = {'events':events}
    return render(request, 'windows/events.html', context)