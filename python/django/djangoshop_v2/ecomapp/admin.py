from django.contrib import admin
from django.http import HttpResponse
from ecomapp.models import Category, Brand, Product, Cart, CartItem, Order




def make_payed(modeladmin, request, queryset):
	# для выпадающего меню в Order
    queryset.update(status='Оплачен')
make_payed.short_description = "Пометить как оплаченные"

class OrderAdmin(admin.ModelAdmin):
	# фильтр статуса в админ панель в Order
	list_filter = ['status']
	list_display = ['id', 'items_in_order' ]
	actions = [make_payed]

	def items_in_order(self, obj):
		items_in_order = '<br>'.join(['Товар - {0} | Кол-во - {1}'. format(item.product.title, item.qty) 
		    for item in obj.items.items.all()])
			
		return items_in_order
	
	items_in_order.allow_tags = True





admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)