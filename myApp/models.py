from django.db import models
from django.db.models import deletion
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import BLANK_CHOICE_DASH, AutoField, CharField


# Create your models here.


class Tag(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class Product(models.Model):
    image = models.ImageField(upload_to='images', blank=True)
    name = models.CharField(max_length=120, null=False)
    description = models.TextField(max_length=200, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    sellingCount = models.IntegerField(null=True, default=0)
    label = models.ForeignKey(Tag, on_delete=CASCADE)
    date = models.DateField

    def __str__(self):
        return f"{self.name} | ${self.price} | - {self.label}"

    def ProductSold(self):
        self.sellingCount += 1
        self.save()


class Cart(models.Model):
    cart_id = models.CharField(primary_key=True, max_length=500)
    products = models.ManyToManyField(Product, through='Product_Cart')
    checkout_total = models.DecimalField(
        max_digits=200, decimal_places=2, blank=True, default=0)

    class Meta:
        ordering = ['cart_id']

    def __str__(self):
        return f"Cart ID: {self.cart_id} | Total Products: {len(self.products.all())}"


class Product_Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    cart = models.ForeignKey(Cart, on_delete=CASCADE)
    quantity = models.IntegerField(max_length=10, blank=True, default=0)
    date_added = models.DateField()

    class Meta:
        unique_together = [['product', 'cart']]


class Month(models.Model):
    month_number = models.AutoField(primary_key=True, unique=True)
    items_sold = models.IntegerField(blank=True, default=0)
    total_revenue = models.DecimalField(
        blank=True, default=0, max_digits=1000000000, decimal_places=2)

    class Meta:
        ordering = ['month_number']

    def sale_item(self, price):
        """
        Note: Please enter price of the perticular product.
        This function will add 1 to items_sold and add price to total_revenue.
        """

        self.items_sold += 1
        self.total_revenue += price
        self.save()
