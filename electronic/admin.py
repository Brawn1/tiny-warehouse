from django.contrib import admin
from .models import AssortmentBox, PartCategory, Part, Compartment


admin.site.register(AssortmentBox)
admin.site.register(PartCategory)
admin.site.register(Part)


class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'part', 'quantity', 'assortment_box')
    search_fields = ('number', 'part__name', 'assortment_box__name')
    list_filter = ('assortment_box', 'part__manufacturer', 'part__category')


admin.site.register(Compartment, CompartmentAdmin)
