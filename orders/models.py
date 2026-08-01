from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"{self.user} - {self.created_at}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product} - {self.quantity} - {self.added_at}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('processing', 'Собирается'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен')
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные при получении'),
        ('card', 'Карта'),
        ('online', 'Онлайн оплата')
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash', verbose_name='Способ оплаты')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')

    delivery_address = models.TextField(verbose_name='Адрес доставки')
    delivery_phone = models.CharField(max_length=15, verbose_name='Телефон доставки')
    delivery_name = models.CharField(max_length=100, verbose_name='Имя получателя')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Итого')
    delivery_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Стоимость доставки')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.pk} - {self.user}"

    @property
    def grand_total(self):
        return self.total_price + self.delivery_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, verbose_name='Товар')
    product_name = models.CharField(max_length=200, verbose_name='Название товара')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    @property
    def total_price(self):
        return self.product_price * self.quantity
