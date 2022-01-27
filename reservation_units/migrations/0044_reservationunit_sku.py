# Generated by Django 3.1.14 on 2022-01-26 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_units', '0043_reservationunit_max_reservations_per_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationunit',
            name='sku',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='SKU'),
        ),
    ]
