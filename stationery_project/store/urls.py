from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # ✅ ADD THESE
    path('cart/', views.cart_page, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', views.remove_item, name='remove'),

    # ✅ LOGIN REGISTER (TEMP SIMPLE)
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('update/<int:id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
]
