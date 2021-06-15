# Generated by Django 3.1.10 on 2021-06-14 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0008_unit_application_validate_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceSectorFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSectorFeatureRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=150, verbose_name='Role name')),
                ('features', models.ManyToManyField(to='permissions.ServiceSectorFeature')),
            ],
        ),
    ]
