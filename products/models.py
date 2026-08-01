from django.db import models

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name='Описание')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Родительская категория',
                               related_name='children')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='products')
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])
    old_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Старая цена', validators=[MinValueValidator(0)],
                                    null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    stock = models.IntegerField(default=0, verbose_name='Наличие')
    unit = models.CharField(max_length=10, verbose_name='Единица измерения', default='шт',
                            choices=[('шт', 'Штука'), ('кг', 'Килограмм'), ('г', 'Грамм'),
                                      ('л', 'Литр'), ('мл', 'Миллилитр'), ('упак', 'Упаковка')])
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    @property
    def discount_percent(self) -> float:
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0

    @property
    def in_stock(self) -> bool:
        return self.stock > 0

    @property
    def avg_rating(self) -> float:
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    @property
    def reviews_count(self) -> int:
        return self.reviews.count()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} | {self.product} | ({self.rating} ⭐)"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    alt = models.CharField('Alt текст', max_length=200, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'
        ordering = ['order']


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by', verbose_name='Товар')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Список желаний'
        verbose_name_plural = 'Списки желаний'
        unique_together = ('user', 'product')