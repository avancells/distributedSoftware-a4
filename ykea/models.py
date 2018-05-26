# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth

# Create your models here.

class Wallet(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.FloatField()

class Item(models.Model):
    CATEGORIES = (
        ("beds", "Beds & mattressess"),
        ("furn", "Furniture, wardrobes & shelves"),
        ("sofa", "Sofas & armchairs"),
        ("table", "Tables & chairs"),
        ("texti","Textiles"),
        ("deco","Decoration & mirrors"),
        ("light","Lighting"),
        ("cook","Cookware"),
        ("tablw","Tableware"),
        ("taps","Taps & sinks"),
        ("org", "Organisers & storage accesories"),
        ("toys","Toys"),
        ("leis","Leisure"),
        ("safe","safety"),
        ("diy", "Do-it-yourself"),
        ("floor","Flooring"),
        ("plant","Plants & gardering"),
        ("food","Food & beverages")
    )
    item_number = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_new = models.BooleanField()
    size = models.CharField(max_length=40)
    instructions = models.FileField(upload_to = "ykea/static/files/", default='ykea/static/files/default.pdf')
    featured_photo = models.ImageField(upload_to = "ykea/static/images/", default='ykea/static/images/default.jpg')
    category = models.CharField(max_length=5, choices=CATEGORIES)
    def __str__(self):
        return  ('[**NEW**]' if self.is_new else '') + "[" + self.category + "] [" + self.item_number + "] " + self.name + " - " + self.description + " (" + self.size + ") : " + str(self.price) + u" €"

class Shoppingcart(models.Model):
    #id_cart = models.CharField(max_length=8, unique=True)
    id_cart = models.AutoField(primary_key = True)
    item_list = models.ManyToManyField(Item, through='Quantity', null=True, blank=True)

class Quantity(models.Model):
    id_quant = models.AutoField(primary_key = True)
    shopping_cart = models.ForeignKey(Shoppingcart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantitat = models.IntegerField()

class Bill(models.Model):
    id_bill = models.AutoField(primary_key = True)
    user = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)

class ItemBill(models.Model):
    id_itemBill = models.AutoField(primary_key = True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantitat = models.IntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)


class ShoppingCounter(models.Model):
    counter = 0

class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
