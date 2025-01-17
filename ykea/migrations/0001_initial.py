# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-26 20:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id_bill', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_number', models.CharField(max_length=8, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_new', models.BooleanField()),
                ('size', models.CharField(max_length=40)),
                ('instructions', models.FileField(default='ykea/static/files/default.pdf', upload_to='ykea/static/files/')),
                ('featured_photo', models.ImageField(default='ykea/static/images/default.jpg', upload_to='ykea/static/images/')),
                ('category', models.CharField(choices=[('beds', 'Beds & mattressess'), ('furn', 'Furniture, wardrobes & shelves'), ('sofa', 'Sofas & armchairs'), ('table', 'Tables & chairs'), ('texti', 'Textiles'), ('deco', 'Decoration & mirrors'), ('light', 'Lighting'), ('cook', 'Cookware'), ('tablw', 'Tableware'), ('taps', 'Taps & sinks'), ('org', 'Organisers & storage accesories'), ('toys', 'Toys'), ('leis', 'Leisure'), ('safe', 'safety'), ('diy', 'Do-it-yourself'), ('floor', 'Flooring'), ('plant', 'Plants & gardering'), ('food', 'Food & beverages')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ItemBill',
            fields=[
                ('id_itemBill', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('quantitat', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ykea.Bill')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ykea.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id_quant', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('quantitat', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ykea.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Shoppingcart',
            fields=[
                ('id_cart', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('item_list', models.ManyToManyField(blank=True, default=None, through='ykea.Quantity', to='ykea.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highlighted', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('money', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='quantity',
            name='shopping_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ykea.Shoppingcart'),
        ),
        migrations.AddField(
            model_name='bill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ykea.Wallet'),
        ),
    ]
