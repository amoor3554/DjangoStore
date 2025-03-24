from store.models import Category

def store_website(request) -> dict:  
    categories = Category.objects.order_by('order')
    return {
        'categories': categories,
    }