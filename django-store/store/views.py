from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.translation import gettext as trans
from django.core.paginator import Paginator
from .models import Product, Slider, Category, Cart

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
    products_all = Product.objects.all()
    where = {}

    if query or category:
        if query:
            where = {'name__icontains': query}
        if category:
            where = {'category_id': category}
            
        products = products_all.filter(**where)

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
    else:
        return redirect('StoreCategory')

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





def check_out(request):
    return render(
        request, 'check_out.html'
    )


def check_out_complete(request):
    return render(
        request, 'check_out_complete.html'
    )