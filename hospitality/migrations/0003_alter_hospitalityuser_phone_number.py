# Generated by Django 4.2.8 on 2023-12-21 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitality', '0002_remove_hospitalityuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalityuser',
            name='phone_number',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
