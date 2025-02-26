# Generated by Django 5.1.2 on 2025-02-26 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_booking_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
