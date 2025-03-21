# Generated by Django 5.1.2 on 2025-03-01 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_order_buy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
