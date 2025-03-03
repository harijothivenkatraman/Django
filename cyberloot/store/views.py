from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, Product, Category, Profile
from .forms import RegisterForm, ProfileForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")  # Redirect after successful registration
    else:
        form = RegisterForm()
    
    return render(request, "store/register.html", {"form": form})

@login_required
def add_to_order(request, pk):
    product = Product.objects.get(pk=pk)
    order, created = Order.objects.get_or_create(user=request.user, product=product)
    if not created:
        order.quantity += 1
        order.save()
    return redirect("product_list")

@login_required
def order_details(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "store/order_details.html", {"orders": orders})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'store/product_list.html', {'products': products, 'categories': categories})
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "store/product_detail.html", {"product": product})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create profile
    return render(request, 'store/profile.html', {'profile': profile})

def category_list(request):
    categories = Category.objects.all()
    return render(request, "store/category_list.html", {"categories": categories})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    products = category.products.all()  # Fetch products for the category
    return render(request, 'store/category_detail.html', {'category': category, 'products': products})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'store/dashboard.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'store/edit_profile.html', {'form': form})