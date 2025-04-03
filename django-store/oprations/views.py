from django.shortcuts import render, redirect
from .forms import UserInfoForm
from store.models import Product, Cart, Order, OrderProduct, Transaction
from .models import Transaction, PaymentMethod
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
import math


def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Stripe)

def paypal_transaction(request):
    transaction = make_transaction(request, PaymentMethod.PayPal)

def make_transaction(request, pm):

    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.item)
        total = 0

        for product in products:
            total += product.price

        if total <= 0:
            return None
        
        return Transaction.objects.create(
            customer=form.cleaned_data,
            total=total,
            session=request.session.session_key,
            payment_method=pm,
            items = cart.item,
            amount= math.ceil(total),
            )



def send_order_mail(order, products):
    msg_html = render_to_string('emails/order.html',
                                {
                                    'order':order,
                                    'products':products,
                                }
                            )
    connection = get_connection()
    send_mail(
        subject='New Order',
        html_message=msg_html,
        message=msg_html,
        from_email='noreply@example.com',
        recipient_list=[order.customer['email']],
        connection=connection,
        )
    connection.close()