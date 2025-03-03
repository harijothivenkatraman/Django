from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),  # List all categories
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('register/', views.register, name='register'),  # Add this line
    path('orders/', views.order_details, name='order_details'),
    path('add_to_order/<int:pk>/', views.add_to_order, name='add_to_order'),
    path('profile/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),  # Profile page
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit profile
]

