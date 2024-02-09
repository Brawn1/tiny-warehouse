from django.contrib import admin
from .models import Manufacturer, Warehouse, AssortmentBox, PartCategory, Part, Compartment

admin.site.register(Manufacturer)
admin.site.register(Warehouse)
admin.site.register(AssortmentBox)
admin.site.register(PartCategory)
admin.site.register(Part)


class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'part', 'quantity', 'assortment_box')
    search_fields = ('number', 'part__name', 'assortment_box__name')


admin.site.register(Compartment, CompartmentAdmin)
