from functools import reduce
from typing import List

from django.db import models
from store.models import Variation


# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

class CartItemManager(models.Manager):
    
    def filter_exact_variations(self, product, cart, variations: List[Variation] = None):
        initial_qs = self.filter(product=product, cart=cart).annotate(cnt=models.Count('variations')).filter(cnt=len(variations))
        
        items = reduce(lambda qs, pk: qs.filter(variations=pk), variations, initial_qs)

        return items

class CartItem(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    variations = models.ManyToManyField('store.Variation', blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    objects = CartItemManager()
    class Meta:
        db_table = 'cart_item'

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
