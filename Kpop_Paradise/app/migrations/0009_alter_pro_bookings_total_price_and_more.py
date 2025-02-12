# Generated by Django 5.1.2 on 2025-02-11 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_pro_bookings_delete_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pro_bookings',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
