from django.db import migrations

def populate_categories(apps, schema_editor):
    Category = apps.get_model('emprendedores', 'Category')
    categories = [
        {'name': 'Plomería', 'description': 'Servicios de plomería y fontanería para el hogar'},
        {'name': 'Electricidad', 'description': 'Instalaciones, mantenimiento y reparaciones eléctricas'},
        {'name': 'Albañilería', 'description': 'Obras menores, reparaciones y construcción en general'},
        {'name': 'Acarreos', 'description': 'Mudanzas, transportes y acarreos locales de mercancías o bienes'},
    ]
    for cat in categories:
        Category.objects.get_or_create(
            name=cat['name'],
            defaults={'description': cat['description']}
        )

def reverse_populate(apps, schema_editor):
    Category = apps.get_model('emprendedores', 'Category')
    Category.objects.filter(name__in=['Plomería', 'Electricidad', 'Albañilería', 'Acarreos']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('emprendedores', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories, reverse_populate),
    ]
