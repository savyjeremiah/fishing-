from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegistrationForm
from .models import Product, Cart, CartItem

# Product View
def product(request):
    smoked_fish = Product.objects.filter(category='smoked_fish')
    ice_fish = Product.objects.filter(category='ice_fish')
    finger_fish = Product.objects.filter(category='finger_fish')

    context = {
        'smoked_fish': smoked_fish,
        'ice_fish': ice_fish,
        'finger_fish': finger_fish,
    }
    return render(request, 'products.html', context)

# User Registration
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

# User Login
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Home View
def home(request):
    return render(request, 'home.html')

# About View
def about(request):
    return render(request, 'about.html')



def services(request):
    return render(request, 'services.html')




@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')  # Redirect to cart detail view or any desired page

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart_detail.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item.quantity = max(1, quantity)
        cart_item.save()
    return redirect('cart_detail')
