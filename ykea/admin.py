from django.contrib import admin
from .models import Item,Shoppingcart,Quantity,Wallet,Bill,ItemBill

# Register your models here.
admin.site.register(Item)

class ShoppingId(admin.ModelAdmin):
    readonly_fields = ('id_cart',)
admin.site.register(Shoppingcart, ShoppingId)

class QuantityId(admin.ModelAdmin):
    readonly_fields = ('id_quant',)
admin.site.register(Quantity, QuantityId)

class WalletId(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(Wallet, WalletId)

class BillId(admin.ModelAdmin):
    readonly_fields = ('id_bill',)
admin.site.register(Bill, BillId)

class ItemBillId(admin.ModelAdmin):
    readonly_fields = ('id_itemBill',)
admin.site.register(ItemBill, ItemBillId)
