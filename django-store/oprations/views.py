from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django_store import settings
from .forms import UserInfoForm
from store.models import Product, Cart, Order
from .models import Transaction, PaymentMethod
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from django.utils.translation import gettext as trans
import math
import stripe
from stripe.error import SignatureVerificationError
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_ENDPOINT_SECRET)

    except ValueError:
        print('Invalid payload')
        return HttpResponse(status=400)
        
    except SignatureVerificationError:
        print('Invalid signature')
        return HttpResponse(status=400)
    
    try:
        print("🔔 Event type received:", event.type)
        # Handle the event
        if event.type == 'payment_intent.succeeded':
            print("📥 Event: payment_intent.succeeded RECEIVED")
            payment_intent = event.data.object
            print("✅ Payment succeeded with ID:", payment_intent.id)
            transaction_id = payment_intent.metadata.transaction
            make_order(transaction_id)

        elif event.type == 'charge.succeeded':
            charge = event.data.object
            print("💰 Charge succeeded:", charge.id)

        else:
            print('Unhandled event type {}'.format(event.type))
        
    except Exception as e:
        import traceback
        print("❌ Exception in webhook:", e)
        traceback.print_exc()
        return HttpResponse(status=500)

    return HttpResponse(status=200)
        
def make_order(transaction_id):
    transaction = Transaction.objects.filter(pk=transaction_id).first()
    order = Order.objects.create(transaction=transaction)
    if transaction:
        order.transaction = transaction
        order.save()
    products = Product.objects.filter(pk__in=transaction.items)
    for product in products:
        order.orderproduct_set.create(product_id=product.id, price=product.price)

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
        recipient_list=[order.transaction.customer_email],
        connection=connection,
        )
    connection.close()


def check_out(request):
    return render(
        request, 'check_out.html'
    )


def check_out_complete(request):
    Cart.objects.filter(session=request.session.session_key).delete()
    return render(
        request, 'check_out_complete.html'
    )


def stripe_config(request):
    return JsonResponse(
        {
            'public_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
    )



def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.STRIPE)
    if not transaction:
        return JsonResponse({'message': trans('Please inter a valid info.')}, status=400)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction': transaction.id
        }
    )
    return JsonResponse({'client_secret': intent["client_secret"]})


def paypal_transaction(request):
    transaction = make_transaction(request, PaymentMethod.PayPal)

def make_transaction(request, pm):

    form = UserInfoForm(request.POST)   
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        if not cart or not hasattr(cart, 'item'):
            return None
        
        products = Product.objects.filter(pk__in=cart.item)
        total = 0

        for product in products:
            total += product.price

        if total <= 0:
            return None
        
        return Transaction.objects.create(
            customer=form.cleaned_data,
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


'''

                                  /////
                ////
    /////////  ////////  //////// /////  ////////////      ////////
  ///////////  ////////  //////// /////  /////////////   ////// /////
  //////       ////      ////     /////  ////     ///// /////     ////
    /////////  ////      ////     /////  ////      //// //////////////
         ///// ////      ////     /////  ////     /////  ////
  ///////////  ////////  ////     /////  /////////////    ///////////
   ////////      //////  ////     /////  //// //////        ///////
                                         ////
                                         ////

'''