# Generated by Django 3.0.10 on 2021-01-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0005_location_relations_to_location_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_map_id', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Service map id')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', max_length=255, verbose_name='Description')),
                ('short_description', models.CharField(blank=True, default='', max_length=255, verbose_name='Short description')),
                ('web_page', models.URLField(blank=True, default='', max_length=255, verbose_name='Homepage for the unit')),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='Telephone')),
            ],
        ),
    ]
