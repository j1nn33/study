from django.contrib import admin

# Register your models here.

from .models import Vch, Author, Sostav


"""Minimal registration of Models.
admin.site.register(Vch)
admin.site.register(Author)
admin.site.register(Sostav)
"""
admin.site.register(Sostav)


class VchAdmin(admin.ModelAdmin):
    list_display = ('number_vch',
                    'okrug',
                    'oblast',
                    'town',
                    'name',
                    'serial',
                    'serial_number',
                    'manager',
    )
    list_filter = ('okrug', 'manager')

class AuthorAdmin(admin.ModelAdmin):

    list_display = ('last_name', 'first_name', 'status')



admin.site.register(Vch, VchAdmin)
admin.site.register(Author, AuthorAdmin)


