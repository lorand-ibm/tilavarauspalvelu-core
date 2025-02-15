# Generated by Django 3.1.14 on 2021-12-13 08:55

from django.db import migrations, models


def add_tax_percentages(apps, schema_editor):
    # Add tax percentages for 0%, 10%, 14% and 24%
    tax_percentages = [0, 10, 14, 24]
    TaxPercentage = apps.get_model('reservation_units', 'TaxPercentage')
    for value in tax_percentages:
        TaxPercentage.objects.create(value=value)


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_units', '0038_reservation_unit_publish_and_reservation_datetimes'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxPercentage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, help_text='The tax percentage for a price', max_digits=5, verbose_name='Tax percentage')),
            ],
        ),
        migrations.RunPython(add_tax_percentages, reverse_code=migrations.RunPython.noop),
    ]
