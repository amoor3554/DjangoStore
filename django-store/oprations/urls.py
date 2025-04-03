from django.urls import path
from . import views
urlpatterns = [
    path('order/stripe', views.stripe_transaction, name='CheckoutStripe'),
    path('order/paypal', views.paypal_transaction, name='CheckoutStripe'),

]
