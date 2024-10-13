from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', index, name='index'),  # Home page
    path('register/',register_page, name='register'),
    path('about/',about_page, name='about'),
    path('login/',login_page, name='login'),
    path('logout/',logoutUser, name='logout'),
    path('windows/',window_list , name='window_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('dashboard/',admin_dashboard, name='dashboard'),
    # path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Product detail
    path('product/create/', product_create, name='product_create'),  # Create a product
    path('product/<int:pk>/edit/', product_update, name='product_update'),  # Edit a product
    path('window/<int:pk>/edit/', window_update, name='window_update'),  # Edit a product
    path('product/<int:pk>/delete/', product_delete, name='product_delete'),  # Delete a product
    path('request-quote/', request_quote, name='request_quote'),  # Quote request page
    path('contact/', contact, name='contact'),  # Contact page
    path('customer/<str:pk>/',customer_page, name='customer_page'),
    path('update-customer/<str:pk>/',update_customer, name='update-customer'),
    path('create-order/<str:pk>/',create_order, name='create-order'),
    path('update-order/<str:pk>/',update_order, name='update-order'),
    path('delete-order/<str:pk>/',delete_order, name='delete-order'),
    path('create-customer/',create_customer, name='create-customer'),
    path('thanks/', thanks, name='thanks'),
    path('gallery/', gallery, name='gallery'),
    path('services/', services, name='services'),
    path('careers/', careers, name='careers'),
    path('upload/', upload_image, name='upload_image'),
    path('door/',doors_list, name='door'),
    path('privacy/',privacy, name='privacy'),
    path('terms-condition/',terms, name='terms'),
    path('code-of-conduct/',codeconduct, name='code-conduct'),
    path('events/',events, name='events'),
    path('log-ip/', record_user_ip, name='log_ip'),
    path('wechat/',wechat,name='wechat')
    # path('<str:lang>/', translate_view, name='translate_home'),  # Language-specific view
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
