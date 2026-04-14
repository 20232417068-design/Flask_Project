from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Cart


# 🏠 HOME PAGE
def home(request):
    if Product.objects.count() == 0:
        Product.objects.create(name="Cover", price=50)
        Product.objects.create(name="Notebook", price=40)
        Product.objects.create(name="Pencil", price=3)
        Product.objects.create(name="Pen", price=5)
        Product.objects.create(name="Glue", price=10)
        Product.objects.create(name="Colour box", price=120)
        Product.objects.create(name="Project Paper", price=50)
        Product.objects.create(name="Sketch book", price=80)
        Product.objects.create(name="Highlighter", price=30)
        Product.objects.create(name="File Folder", price=350)
        Product.objects.create(name="Calculator", price=250)
        Product.objects.create(name="Eraser", price=3)
        Product.objects.create(name="Stapler", price=60)
        Product.objects.create(name="Long scale", price=40)
        Product.objects.create(name="Scissors", price=40)
        Product.objects.create(name="Marker", price=300)
       
    query = request.GET.get('q')

    if query is not None and query.strip() != "":
        products = Product.objects.filter(name__icontains=query)
    else:

       products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# 🔐 LOGIN
def login_view(request):

    if request.method == "GET":
        if request.GET.get('next'):
            messages.warning(request, "⚠️ Please login first to continue!")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ EMPTY FIELD CHECK
        if not username or not password:
            messages.error(request, "⚠️ Please enter username and password!")
            return redirect('/login/')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('/')
        else:
            messages.error(request, "❌ Invalid username or password!")

    return render(request, 'login.html')


# 📝 REGISTER
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "⚠️ Please fill all fields!")
            return redirect('/register/')

        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Username already exists!")
            return redirect('/register/')

        User.objects.create_user(username=username, password=password)

        messages.success(request, "🎉 You have registered successfully!")
        return redirect('/register/')

    return render(request, 'register.html')


# 🛒 ADD TO CART (FINAL FIX)
@login_required(login_url='/login/')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# 📦 CART PAGE
@login_required(login_url='/login/')
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ❌ REMOVE ITEM
@login_required(login_url='/login/')
def remove_item(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('cart')


# 🔄 UPDATE QUANTITY
@login_required(login_url='/login/')
def update_quantity(request, id, action):
    cart_item = Cart.objects.get(id=id)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return redirect('cart')

    cart_item.save()
    return redirect('cart')


# 🧾 CHECKOUT
@login_required(login_url='/login/')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        name = request.POST.get("name")

        cart_items.delete()

        return render(request, "success.html", {
            "name": name
        })

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })


# 💳 PAYMENT
@login_required(login_url='/login/')
def payment(request):
    return render(request, 'payment.html')