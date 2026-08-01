import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product

User = get_user_model()

# Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@djangomart.uz', 'admin123', first_name='Admin')
    print("✅ Superuser created: admin / admin123")

# Categories
cats_data = [
    ('Фрукты и ягоды', 'fruits', 'Свежие фрукты и ягоды'),
    ('Овощи и зелень', 'vegetables', 'Свежие овощи и зелень'),
    ('Молочные продукты', 'dairy', 'Молоко, сыр, йогурт'),
    ('Мясо и птица', 'meat', 'Свежее мясо и птица'),
    ('Хлеб и выпечка', 'bakery', 'Свежая выпечка'),
    ('Напитки', 'drinks', 'Соки, воды, газировка'),
    ('Крупы и макароны', 'grains', 'Рис, гречка, макаронные изделия'),
    ('Сладости', 'sweets', 'Конфеты, шоколад, торты'),
]

categories = {}
for name, slug, desc in cats_data:
    cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
    categories[slug] = cat
    print(f"📁 Category: {name}")

# Products
products_data = [
    # fruits
    ('Яблоки Голден', 'apples-golden', 'fruits', 8900, 10000, 100, 'кг', True, True),
    ('Бананы', 'bananas', 'fruits', 12000, None, 80, 'кг', True, False),
    ('Апельсины', 'oranges', 'fruits', 15000, 18000, 60, 'кг', False, True),
    ('Клубника', 'strawberry', 'fruits', 25000, None, 40, 'кг', True, True),
    # vegetables
    ('Помидоры', 'tomatoes', 'vegetables', 9000, None, 120, 'кг', True, False),
    ('Огурцы', 'cucumbers', 'vegetables', 7000, 9000, 150, 'кг', False, False),
    ('Картофель', 'potatoes', 'vegetables', 4000, None, 200, 'кг', True, False),
    ('Морковь', 'carrots', 'vegetables', 5000, None, 180, 'кг', False, False),
    # dairy
    ('Молоко 3.5%', 'milk-35', 'dairy', 11000, None, 90, 'л', True, False),
    ('Сыр Российский', 'cheese-russian', 'dairy', 35000, 40000, 50, 'кг', False, True),
    ('Йогурт натуральный', 'yogurt-natural', 'dairy', 8500, None, 70, 'упак', True, False),
    # meat
    ('Куриная грудка', 'chicken-breast', 'meat', 45000, 52000, 60, 'кг', True, True),
    ('Говядина (вырезка)', 'beef-fillet', 'meat', 95000, None, 30, 'кг', False, False),
    # bakery
    ('Хлеб белый', 'white-bread', 'bakery', 6000, None, 100, 'шт', True, False),
    ('Круассан с маслом', 'croissant', 'bakery', 8000, None, 50, 'шт', False, True),
    # drinks
    ('Вода Nestle 1.5л', 'water-nestle', 'drinks', 7000, None, 200, 'шт', True, False),
    ('Сок яблочный 1л', 'juice-apple', 'drinks', 14000, 16000, 80, 'шт', False, False),
    # grains
    ('Рис длиннозёрный', 'rice-long', 'grains', 18000, None, 150, 'кг', True, False),
    ('Макароны спагетти', 'spaghetti', 'grains', 12000, 14000, 100, 'упак', False, True),
    # sweets
    ('Шоколад Milka 100г', 'milka-chocolate', 'sweets', 22000, 26000, 60, 'шт', True, True),
]

for name, slug, cat_slug, price, old_price, stock, unit, featured, is_new in products_data:
    p, _ = Product.objects.get_or_create(slug=slug, defaults={
        'name': name,
        'category': categories[cat_slug],
        'price': price,
        'old_price': old_price,
        'stock': stock,
        'unit': unit,
        'is_featured': featured,
        'is_new': is_new,
        'description': f'Качественный продукт — {name}. Свежий, натуральный.',
    })
    print(f"🛒 Product: {name}")

print("\n✅ Seed completed!")
print(f"   Products: {Product.objects.count()}")
print(f"   Categories: {Category.objects.count()}")
