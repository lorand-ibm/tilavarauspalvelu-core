# Generated by Django 3.1.7 on 2021-03-19 11:45

from django.db import migrations, models

def update_permissions(apps, schema_editor):
    GeneralRoleChoice = apps.get_model('permissions', 'GeneralRoleChoice')
    GeneralRolePermission = apps.get_model('permissions', 'GeneralRolePermission')


    # General Admin
    general_admin = GeneralRoleChoice.objects.get(
        code="admin",
    )
    GeneralRolePermission.objects.create(
        role=general_admin,
        permission="can_modify_cities"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0006_allocation_permissions'),
    ]

    operations = [
        migrations.RunPython(update_permissions, migrations.RunPython.noop),
    ]
