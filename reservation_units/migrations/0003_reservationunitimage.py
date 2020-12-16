# Generated by Django 3.0.10 on 2020-12-07 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_units', '0002_purpose_related_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationUnitImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_type', models.CharField(choices=[('main', 'Main image'), ('ground_plan', 'Ground plan'), ('map', 'Map'), ('other', 'Other')], max_length=20, verbose_name='Type')),
                ('image_url', models.URLField(max_length=255, verbose_name='Image url')),
                ('reservation_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='reservation_units.ReservationUnit', verbose_name='Reservation unit image')),
            ],
        ),
    ]
