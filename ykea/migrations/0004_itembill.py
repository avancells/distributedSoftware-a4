# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-13 11:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ykea', '0003_auto_20180513_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemBill',
            fields=[
                ('id_itemBill', models.AutoField(primary_key=True, serialize=False)),
                ('quantitat', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ykea.Bill')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ykea.Item')),
            ],
        ),
    ]
