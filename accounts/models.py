from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(unique=True, blank=True, max_length=20, verbose_name='Телефон')
    delivery_address = models.TextField(blank=True, verbose_name='Адрес доставки')
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True, verbose_name="Аватар")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
