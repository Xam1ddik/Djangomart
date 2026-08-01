from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import Cart, CartItem


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'components/cart.html', {'cart': cart})


@login_required
def cart_add_view(request, pk):
    product = get_object_or_404(Product, id=pk, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f'«{product.name}» добавлен в корзину.')

    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        return redirect(referrer)
    return redirect('cart_url')




@login_required
def cart_update_view(request, pk):
    item = get_object_or_404(CartItem, id=pk, cart__user=request.user)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        if quantity < 1:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

    return redirect('cart_url')


@login_required
def cart_remove_view(request, pk):
    item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
    item.delete()
    messages.info(request, 'Товар удалён из корзины.')
    return redirect('cart_url')


@login_required
def cart_clear_view(request):
    Cart.objects.filter(user=request.user).delete()
    messages.info(request, 'Корзина очищена.')
    return redirect('cart_url')