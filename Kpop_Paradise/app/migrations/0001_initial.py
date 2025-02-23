# Generated by Django 5.1.5 on 2025-02-04 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='bands/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total_ticket', models.PositiveIntegerField(default=100)),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concerts', to='app.band')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('quantity', models.PositiveIntegerField()),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='app.concert')),
            ],
        ),
    ]
