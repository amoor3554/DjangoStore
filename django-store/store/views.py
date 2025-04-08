from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.utils.translation import gettext as trans
from django.core.paginator import Paginator
from .models import Product, Slider, Category, Cart
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
    product = Product.objects.get(pk=pid)
    return render(
        request, 'product.html',
        {
            'product': product,
        }
    )

def search_product(request):

    query = request.GET.get('query', None)
    category = request.GET.get('category', None)

    if not (query or category):
        return redirect('StoreCategory')
    
    filters = Q(name__icontains=query) | Q(description__icontains=query)

    if category:
        filters &= Q(category_id=category) 
    
    products = Product.objects.filter(filters)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'common/search_product.html',
        {
            'page_obj': page_obj,
            'category': category,
            'query': query,
        }
    )

        
    
def category(request, cid=None):
        
    cat = None
    query = request.GET.get('query', cid)
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

def cart_update(request, pid=None):

    if not request.session.session_key:
        request.session.create()
    
    session_id = request.session.session_key
    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        cart_model = Cart.objects.create(session_id=session_id, item=[pid])
    elif pid not in cart_model.item:
        cart_model.item.append(pid)
        cart_model.save()

    return JsonResponse(
        {
            'message': trans('Item added to cart'),
            'items_count': len(cart_model.item),
        }
    )

def cart_remove(request, pid=None):
    session_id = request.session.session_key

    if not session_id:
        return JsonResponse({})

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        return JsonResponse({})
    
    elif pid in cart_model.item:
        cart_model.item.remove(pid)
        cart_model.save()

    return JsonResponse(
        {
            'message': trans('Item removed from the cart'),
            'items_count': len(cart_model.item),
        }
    )




