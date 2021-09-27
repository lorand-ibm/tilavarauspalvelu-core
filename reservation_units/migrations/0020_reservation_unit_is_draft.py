# Generated by Django 3.1.13 on 2021-09-22 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_units', '0019_equipment_category_name_translations'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationunit',
            name='is_draft',
            field=models.BooleanField(blank=True, db_index=True, default=False, verbose_name='Is this in draft state'),
        ),
    ]
