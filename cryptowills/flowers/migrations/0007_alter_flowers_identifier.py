# Generated by Django 3.2.15 on 2022-08-19 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0006_alter_flowers_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowers',
            name='identifier',
            field=models.CharField(max_length=50),
        ),
    ]
