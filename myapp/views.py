from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

def homeview(request):
    items = Items.objects.all()
    categories = Item_list.objects.all()
    feedbacks = Feedback.objects.all()  # Fetch all feedback
    bookings = Booktable.objects.all()
    return render(request, 'home.html', {
        'items': items,
        'categories': categories,
        'feedbacks': feedbacks,  # Pass feedback to the template
        'bookings': bookings
    })

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required

@login_required
def menuview(request):
    selected_category = request.GET.get('category')

    if selected_category:
        items = Items.objects.filter(categeory__categeory_name=selected_category)
    else:
        items = Items.objects.all()

    categories = Item_list.objects.all()

    # Fetch only the current user's cart items
    cart_items = set(Cart.objects.filter(user=request.user).values_list('item_id', flat=True))

    return render(request, 'menu.html', {
        'items': items,
        'categories': categories,
        'selected_category': selected_category,
        'cart_items': cart_items  # Pass only the logged-in user's cart items
    })



def aboutview(request):
    return render(request, 'about.html')

def booktableview(request):
    if request.method == 'POST':
        form = BooktableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_table')
        else:
            return render(request, 'book.html', {'form': form, 'errors': form.errors})  # Pass errors to template
    else:
        form = BooktableForm()
    return render(request, 'book.html', {'form': form})

def feedbackview(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if feedback.rating is None:  # Provide default rating if missing
                feedback.rating = 5  
            feedback.save()
            return redirect('home')  # Redirect to home page after submission
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def signupview(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logs the user in automatically
            return redirect('home')  # Redirect to the home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})




def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Items, id=item_id)  # Get the item
    # Check if the item is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1  # Increase quantity if item already exists
        cart_item.save()
    return redirect('menu')  # Redirect back to the menu page


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)  # Get cart items for the logged-in user
    total_price = sum(item.item.price * item.quantity for item in cart_items)  # Calculate total price
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1  # Decrease quantity by 1
        cart_item.save()
    else:
        cart_item.delete()  # Delete the item if quantity is 1
    return redirect('cart')


@login_required
def remove_all_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()  # Delete the entire cart item
    return redirect('cart')

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.quantity += 1  # Increase quantity by 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1  # Decrease quantity by 1
        cart_item.save()
    else:
        cart_item.delete()  # Delete the item if quantity is 1
    return redirect('cart')
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout
# views.py
@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})
def order_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'order_page.html', context)
@login_required
def send_email_to_user(request):
    subject = 'Welcome to Feane!'
    message = f'Hello {request.user.username},\n\nThank you for visiting Feane! We hope you enjoy our services.\n\nBest Regards,\nFeane Team'
    recipient_email = request.user.email

    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

    return render(request, 'email_sent.html', {'email': recipient_email})
