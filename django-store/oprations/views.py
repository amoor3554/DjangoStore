from django.shortcuts import render, redirect
from .forms import UserInfoForm
from store.models import Product, Cart, Order, OrderProduct
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string


def make_order(request):
    if request.method != 'POST':
        return redirect('StoreCheckout')

    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.item)
        total = 0

        for product in products:
            total += product.price

        if total <= 0:
            return redirect('StoreCart')
        
        order = Order.objects.create(customer=form.cleaned_data,total=total)

        for product in products:
            OrderProduct.objects.create(product_id=product.id,order=order, price=product.price)
        
        send_order_mail(order=order, products=products)
        cart.delete()
        return redirect('StoreOrderSuccess')
    else:
        return redirect('StoreCheckout')
    

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