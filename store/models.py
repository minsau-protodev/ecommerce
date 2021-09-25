from django.urls import reverse
from category.models import Category
from django.db import models


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='photos/products', blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(is_active=True)

    def sizes(self):
        return self.all().filter(variation_category='size')

    def colors(self):
        return self.all().filter(variation_category='color')

variation_category_choices = (
    ('size', 'Size'),
    ('color', 'Color'),
)
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return f"{self.product} ({self.variation_value})"