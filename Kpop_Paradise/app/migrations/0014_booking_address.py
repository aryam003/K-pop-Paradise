# Generated by Django 5.1.2 on 2025-02-26 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_userprofile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
