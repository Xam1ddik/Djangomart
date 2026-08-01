import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    in_stock = django_filters.BooleanFilter(field_name='stock', lookup_expr='gt', label='Только в наличии')
    has_discount = django_filters.BooleanFilter(method='filter_has_discount', label='Со скидкой')

    class Meta:
        model = Product
        fields = ['category', 'is_featured', 'is_new', 'unit']

    def filter_has_discount(self, queryset, name, value):
        if value:
            return queryset.exclude(old_price__isnull=True)
        return queryset
