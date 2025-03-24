from django.shortcuts import render
from .models import Product, Slider

def index(request):
    products = Product.objects.select_related('author').filter(featured=True)
    slider = Slider.objects.order_by('order')
    return render(
        request, 'index.html',
        {
            'products': products,
            'slides': slider,
        }
    )


def product(request, pid):
    return render(
        request, 'product.html'
    )


def category(request, cid=None):
    return render(
        request, 'category.html'
    )


def cart(request):
    return render(
        request, 'cart.html'
    )


def check_out(request):
    return render(
        request, 'check_out.html'
    )


def check_out_complete(request):
    return render(
        request, 'check_out_complete.html'
    )