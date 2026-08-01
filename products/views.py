from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Category, Product, Review, Wishlist
from products.forms import ReviewForm
from products.filters import ProductFilter
from products.search import build_search_slug, matches, normalize


def index_view(request):
    categories = Category.objects.filter(is_active=True, parent=None).order_by('order', 'name')
    featured_products = Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:8]
    products = Product.objects.filter(is_active=True).select_related('category')
    filterset = ProductFilter(request.GET, queryset=products)

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(
            Wishlist.objects.filter(user=request.user, product__is_active=True).values_list('product_id', flat=True)
        )

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'filter': filterset,
        'product_list': filterset.qs,
        'wishlists': {'product_id': wishlist_product_ids},
    }

    return render(request, 'components/index.html', context)


def category_detail_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    product_list = Product.objects.filter(is_active=True, category=category).select_related('category')
    filterset = ProductFilter(request.GET, queryset=product_list)

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(
            Wishlist.objects.filter(user=request.user, product__is_active=True).values_list('product_id', flat=True)
        )

    context = {
        'category': category,
        'filter': filterset,
        'product_list': filterset.qs,
        'wishlists': {'product_id': wishlist_product_ids},
    }
    return render(request, 'components/category_detail.html', context)


def product_detail_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    reviews = product.reviews.select_related('user').order_by('-created_at')

    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, product=product).exists()

    form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'is_wishlisted': is_wishlisted,
    }
    return render(request, 'components/product_detail.html', context)


def search_views(request):
    q = (request.GET.get('q') or '').strip()
    q_normalized = normalize(q)
    q_slug = build_search_slug(q)

    navbar_categories = Category.objects.filter(is_active=True, parent=None).order_by('order', 'name')

    products = Product.objects.none()
    found_categories = Category.objects.none()

    if q:
        product_ids = [
            product.id
            for product in Product.objects.filter(is_active=True).select_related('category')
            if matches(
                q_normalized, q_slug,
                product.name, product.description, product.category.name,
                slug=product.slug,
            )
        ]
        products = (
            Product.objects.filter(id__in=product_ids)
            .select_related('category')
        )

        category_ids = [
            category.id
            for category in Category.objects.filter(is_active=True)
            if matches(q_normalized, q_slug, category.name, category.description, slug=category.slug)
        ]
        found_categories = Category.objects.filter(id__in=category_ids)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    product_page = paginator.get_page(page_number)

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(
            Wishlist.objects.filter(user=request.user, product__is_active=True).values_list('product_id', flat=True)
        )

    context = {
        'q': q,
        'categories': navbar_categories,
        'found_categories': found_categories,
        'product_page': product_page,
        'products_count': paginator.count,
        'wishlists': {'product_id': wishlist_product_ids},
    }

    return render(request, 'components/search.html', context)


@login_required
def review_add_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            existing = Review.objects.filter(product=product, user=request.user).first()
            if existing:
                existing.rating = form.cleaned_data['rating']
                existing.comment = form.cleaned_data['comment']
                existing.save()
                messages.success(request, 'Ваш отзыв обновлён.')
            else:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Отзыв добавлен.')
        else:
            messages.error(request, 'Проверьте правильность заполнения отзыва.')

    return redirect('product_detail', product_slug=product.slug)


@login_required
def wishlist_view(request):
    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(
            Wishlist.objects.filter(user=request.user, product__is_active=True).values_list('product_id', flat=True)
        )
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    context = {
        'wishlist_items': wishlist_items,
        'wishlists': {'product_id': wishlist_product_ids},
    }

    return render(request, 'components/wishlist.html', context)


@login_required
def wishlist_toggle_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        item.delete()
        messages.info(request, f'«{product.name}» удалён из избранного.')
    else:
        messages.success(request, f'«{product.name}» добавлен в избранное.')

    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        return redirect(referrer)
    return redirect('wishlist_toggle_url')


@login_required
def wishlist_clean_view(request):
    Wishlist.objects.filter(user=request.user).delete()
    messages.info(request, 'Список избранного очищен.')
    return redirect('wishlist_url')
