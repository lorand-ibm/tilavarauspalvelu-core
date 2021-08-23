# Generated by Django 3.1.13 on 2021-08-23 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0014_unit_rename_service_map_id_to_tprek_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='code',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='Code for the space'),
        ),
    ]
