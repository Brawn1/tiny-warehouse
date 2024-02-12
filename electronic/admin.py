from django import forms
from django.contrib import admin
from .models import AssortmentBox, PartCategory, Part, Compartment


admin.site.register(AssortmentBox)
admin.site.register(PartCategory)
admin.site.register(Part)


class CompartmentForm(forms.ModelForm):
    class Meta:
        model = Compartment
        fields = ['number', 'part', 'quantity', 'assortment_box']

    def __init__(self, *args, **kwargs):
        super(CompartmentForm, self).__init__(*args, **kwargs)
        query = Compartment.objects.all().latest('id')
        self.fields['number'].initial = query.number + 1
        self.fields['assortment_box'].initial = query.assortment_box


class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'part', 'quantity', 'assortment_box')
    search_fields = ('number', 'part__name', 'assortment_box__name')
    list_filter = ('assortment_box', 'part__manufacturer', 'part__category')
    form = CompartmentForm


admin.site.register(Compartment, CompartmentAdmin)
