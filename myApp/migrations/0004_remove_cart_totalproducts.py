# Generated by Django 3.2.6 on 2021-08-29 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_remove_product_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='totalProducts',
        ),
    ]
