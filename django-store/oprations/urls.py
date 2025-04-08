from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_out, name='StoreCheckout'),
    path('complete/', views.check_out_complete, name='CheckoutComplete'),
    path('stripe/', views.stripe_transaction, name='CheckoutStripe'),
    path('stripe/config/', views.stripe_config, name='CheckoutStripeConfig'),
    path('stripe/webhook',views.stripe_webhook, name='CheckoutStripeWebhook'),
    #path('paypal/', views.paypal_transaction, name=''),

]
