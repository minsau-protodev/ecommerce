from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from store.models import Product


def paginate_products(request, products):
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    return paged_products

# Create your views here.
def index(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        products_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        products_count = products.count()
        
    context = {
        'products': paginate_products(request, products),
        'products_count': products_count
    }
    return render(request, 'store/index.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e

    context = {
        'product': product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context=context)


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(
        Q(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )
    )
    products_count = products.count()
    context = {
        'products': paginate_products(request, products),
        'products_count': products_count
    }
    return render(request, 'store/index.html', context)
