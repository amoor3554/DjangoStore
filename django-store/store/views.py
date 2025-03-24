from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Slider, Category

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

    cat = None
    where = {}

    if cid:
        cat = Category.objects.get(pk=cid)
        where['category_id'] = cid

    products = Product.objects.filter(**where)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'category.html',
        {
            'page_obj': page_obj,
            'category': cat,
        }
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