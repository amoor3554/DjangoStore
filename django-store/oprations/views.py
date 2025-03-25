from django.shortcuts import render, redirect
from .forms import UserInfoForm
from store.models import Product, Cart, Order, OrderProduct

def make_order(request):
    if request.method != 'POST':
        return redirect('StoreCheckout')

    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.item)
        total = 0

        for item in products:
            total += item.price

        if total <= 0:
            return redirect('StoreCart')
        
        order = Order.objects.create(customer=form.cleaned_data,total=total)

        for product in products:
            OrderProduct.objects.create(product_id=product.id,order=order, price=product.price)
            
        cart.delete()
        return redirect('StoreOrderSuccess')
    else:
        return redirect('StoreCheckout')