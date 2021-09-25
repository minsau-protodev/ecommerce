from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, Variation

from .models import Cart, CartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def index(request, total=0, quantity=0):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax= float(total) * 0.0875
        grand_total = float(total) + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total
    }
    
    return render(request, 'carts/index.html', context=context)

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    variations = []
    if request.method == 'POST':
        color_variation = Variation.objects.get(product=product, variation_category='color', variation_value=request.POST['color'])
        size_variation = Variation.objects.get(product=product, variation_category='size', variation_value=request.POST['size'])
        variations.append(color_variation)
        variations.append(size_variation)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    cart_items = CartItem.objects.filter_exact_variations(
        product=product, cart=cart, variations=variations
    )
    
    if cart_items.exists():
        cart_item = cart_items.first()
        cart_item.quantity += 1
        cart_item.save()
        
        return redirect('cart')
        
    cart_item = CartItem.objects.create(
        product=product,
        quantity=1,
        cart=cart
    )

    cart_item.variations.set(variations)    
    cart_item.save()

    return redirect('cart')



def decrease_cart(_, cart_item):
    cart_item = CartItem.objects.get(id=cart_item)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def increase_cart(_, cart_item):
    cart_item = CartItem.objects.get(id=cart_item)

    if cart_item.product.stock > 1:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def remove_item(_, cart_item):
    cart_item = CartItem.objects.get(id=cart_item)
    cart_item.delete()

    return redirect('cart')