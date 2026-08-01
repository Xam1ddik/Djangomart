from django.urls import path

from products.views import (wishlist_clean_view, category_detail_view, product_detail_view, search_views,
                            review_add_view, wishlist_view, wishlist_toggle_view)

urlpatterns = [
    path('category/<slug:category_slug>/', category_detail_view, name='category_detail'),
    path('product/<slug:product_slug>/', product_detail_view, name='product_detail'),
    path('search/', search_views, name='search_url'),
    path('product/<slug:product_slug>/review/', review_add_view, name='review_add_url'),

    path('wishlist/', wishlist_view, name='wishlist_url'),
    path('wishlist/toggle/<int:product_id>/', wishlist_toggle_view, name='wishlist_toggle_url'),
    path('wishlist/clean/', wishlist_clean_view, name='wishlist_clean_url'),
]
