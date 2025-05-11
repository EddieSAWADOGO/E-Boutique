from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.urls import reverse
from django.contrib import messages

from store.models import Product, Cart, Order
from django.db.models import Sum, F

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from .models import Product, Order, Cart
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .password_reset import account_activation_token

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product": product})

def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False,
                                                 product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    try:
        #une logique pour afficher un message lors des ajouts au panier
        messages.success(request, "Produit ajouté au panier avec succès!")
    except Exception as e:
        messages.error(request,f"Erreur : {str(e)}")

    return redirect(reverse("product", kwargs={"slug": slug}))

def cart(request):
    # Récupération du panier avec préfetch_related pour optimiser les requêtes
    cart = get_object_or_404(
        Cart.objects.prefetch_related('orders__product'),
        user=request.user
    )

    # Calcul du total général avec annotation
    total_price = cart.orders.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    ).get('total') or 0

    # Ajout des sous-totaux pour chaque produit
    orders = cart.orders.annotate(
        subtotal=F('quantity') * F('product__price')
    )

    context = {
        'orders': orders,
        'total_price': total_price
    }

    return render(request, 'store/cart.html', context)

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()

    return redirect('index')

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, "Article supprimé du panier avec succès!")
    return redirect('cart')
