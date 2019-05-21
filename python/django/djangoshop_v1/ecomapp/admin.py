from django.contrib import admin
from ecomapp.models import Category, Brand, Product, Cart, CartItem, Order




def make_payed(modeladmin, request, queryset):
	# для выпадающего меню в Order
    queryset.update(status='Оплачен')
make_payed.short_description = "Пометить как оплаченные"

class OrderAdmin(admin.ModelAdmin):
	# фильтр статуса в админ панель в Order
	list_filter = ['status']
	actions = [make_payed]





admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)