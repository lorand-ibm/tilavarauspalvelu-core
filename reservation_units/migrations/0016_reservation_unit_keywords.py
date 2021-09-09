# Generated by Django 3.1.13 on 2021-09-09 08:35

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_units', '0015_reservation_unit_max_and_min_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='reservation_units.keyword', verbose_name='Parent keyword')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reservationunit',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='reservation_units', to='reservation_units.Keyword', verbose_name='Keywords'),
        ),
    ]
