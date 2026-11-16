from django.urls import path
from .views import send_email_to_user
from .views import homeview, menuview, aboutview, booktableview, feedbackview,signupview,profile_view,order_page,loginview,cart_view,add_to_cart,remove_from_cart,logout_view,remove_all_from_cart,increase_quantity,decrease_quantity

urlpatterns = [
    path('', homeview, name="home"),
    path('menu/', menuview, name="menu"),
    path('about/', aboutview, name="about"),
    path('book_table/', booktableview, name="book_table"),
    path('feedback/', feedbackview, name="feedback"),
    path('signup/', signupview, name='signup'),
    path('login/', loginview, name='login'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'), 
    path('increase-quantity/<int:cart_item_id>/', increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:cart_item_id>/', decrease_quantity, name='decrease_quantity'),
     path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('remove-all-from-cart/<int:cart_item_id>/', remove_all_from_cart, name='remove_all_from_cart'),
    path('logout/', logout_view, name='logout'),
    # urls.py
    path('profile/', profile_view, name='profile'),
    path('order/', order_page, name='order_page'),
    path('send-email/', send_email_to_user, name='send_email'),

     
]
