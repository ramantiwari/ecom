# Generated by Django 5.1.6 on 2025-03-02 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0002_banner_headercategorydetails_alter_customer_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('pillow block bearings', 'Pillow Block Bearings'), ('rod ends', 'Rod Ends'), ('pneumatics parts', 'Pneumatics Parts'), ('motors&gearbox', 'Motors&Gearbox'), ('office supply', 'Office Supply'), ('product1', 'Product1'), ('Contactors&Contacts', 'contactors&contacts'), ('photoelectric sensors', 'Photoelectric Sensors')], max_length=256),
        ),
    ]
