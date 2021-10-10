# Generated by Django 3.2.6 on 2021-08-29 04:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('totalProducts', models.IntegerField(blank=True, default=0, max_length=200)),
                ('checkout_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=200)),
            ],
            options={
                'ordering': ['cart_id'],
            },
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('month_number', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('items_sold', models.IntegerField(blank=True, default=0)),
                ('total_revenue', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=1000000000)),
            ],
            options={
                'ordering': ['month_number'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sellingCount', models.IntegerField(default=0, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, max_length=10)),
                ('date_added', models.DateField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.tag'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='myApp.Product_Cart', to='myApp.Product'),
        ),
    ]
