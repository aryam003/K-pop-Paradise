# Generated by Django 5.1.2 on 2025-03-02 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_buy_total_price_alter_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='concert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='app.concert'),
        ),
    ]
