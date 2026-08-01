from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, Review, Wishlist


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border-radius: 8px; object-fit: cover;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = 'Изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'parent',
        'is_active',
        'order',
        'image_preview',
        'created_at'
    )
    list_display_links = ('id', 'name')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    ordering = ('order', 'name')
    list_editable = ('is_active', 'order')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview')
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border-radius: 8px; object-fit: cover;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = 'Изображение'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'old_price',
        'discount_percent',
        'stock',
        'unit',
        'in_stock',
        'avg_rating',
        'reviews_count',
        'is_active',
        'is_featured',
        'is_new',
        'image_preview',
        'created_at'
    )
    list_display_links = ('id', 'name')
    list_filter = (
        'category', 'unit', 'is_active', 'is_featured', 'is_new', 'created_at'
    )
    search_fields = ('name', 'slug', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = (
        'created_at', 'updated_at', 'discount_percent', 'in_stock', 'avg_rating', 'reviews_count', 'image_preview'
    )
    list_editable = (
        'price', 'stock', 'is_active', 'is_featured', 'is_new'
    )
    ordering = ('-created_at',)
    list_per_page = 20
    inlines = [ProductImageInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Цена', {
            'fields': ('price', 'old_price', 'discount_percent')
        }),
        ('Склад', {
            'fields': ('stock', 'unit', 'in_stock')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview')
        }),
        ('Статусы', {
            'fields': ('is_active', 'is_featured', 'is_new')
        }),
        ('Рейтинг и отзывы', {
            'fields': ('avg_rating', 'reviews_count'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = 'Изображение'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'user',
        'rating_stars',
        'comment_short',
        'created_at'
    )
    list_display_links = ('id', 'product')
    list_filter = ('rating', 'created_at')
    search_fields = (
        'product__name',
        'user__username',
        'comment'
    )
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 20

    def rating_stars(self, obj):
        return "⭐" * obj.rating

    rating_stars.short_description = 'Оценка'

    def comment_short(self, obj):
        if obj.comment:
            return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
        return "Без комментария"

    comment_short.short_description = 'Комментарий'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'image_preview',
        'alt',
        'order'
    )
    list_display_links = ('id', 'product')
    list_filter = ('product',)
    search_fields = ('product__name', 'alt')
    readonly_fields = ('image_preview',)
    list_editable = ('order',)
    ordering = ('product', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Превью"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'added_at'
    )
    list_display_links = ('id', 'user')
    list_filter = ('added_at',)
    search_fields = (
        'user__username',
        'product__name'
    )
    readonly_fields = ('added_at',)
    ordering = ('-added_at',)
    list_per_page = 20
