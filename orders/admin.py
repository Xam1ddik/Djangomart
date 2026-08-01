from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at', 'total_price')
    autocomplete_fields = ('product', )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline, )

    list_display = (
        'id',
        'user',
        'total_items',
        'total_price',
        'created_at',
        'updated_at'
    )

    list_filter = ('created_at', 'updated_at')

    search_fields = ('user__username', 'user__email',
                     'user__first_name', 'user__last_name')

    readonly_fields = ('total_items', 'total_price',
                       'created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'product',
        'quantity',
        'added_at',
        'total_price'
    )

    list_filter = ('added_at', )

    search_fields = (
        'cart__user__username',
        'cart__user__email',
        'cart__user__first_name',
        'cart__user__last_name',
        'product__name'
    )

    readonly_fields = ('added_at', 'total_price')

    autocomplete_fields = ('cart', 'product')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ('product', )
    readonly_fields = ('total_price', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, )
    list_display = (
        'id',
        'user',
        'status',
        'payment_method',
        'is_paid',
        'total_price',
        'delivery_price',
        'grand_total',
        'created_at'
    )

    list_display_links = ('id', 'user')

    list_editable = ('status', 'is_paid')

    list_filter = (
        'status',
        'payment_method',
        'is_paid',
        'created_at',
        'updated_at'
    )

    search_fields = (
        'id',
        'user__username',
        'user__email',
        'delivery_name',
        'delivery_phone',
        'delivery_address'
    )

    readonly_fields = ('created_at', 'updated_at', 'grand_total')
    autocomplete_fields = ('user', )

    date_hierarchy = 'created_at'

    ordering = ('-created_at', )

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'user',
                'status',
                'payment_method',
                'is_paid'
            )
        }),
        ('Доставка', {
            'fields': (
                'delivery_name',
                'delivery_phone',
                'delivery_address',
                'comment'
            )
        }),
        ('Стоимость', {
            'fields': (
                'total_price',
                'delivery_price',
                'grand_total'
            )
        }),
        ('Даты', {
            'fields': (
                'created_at',
                'updated_at'
            )
        })
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'product_name',
        'product_price',
        'quantity',
        'total_price'
    )

    list_filter = ('order__status',)
    search_fields = (
        'id',
        'order__id',
        'product__name',
        'product_name'
    )
    autocomplete_fields = ('order', 'product')
    readonly_fields = ('total_price',)
