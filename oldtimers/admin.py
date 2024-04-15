from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from .models import StorageLocation, Vehicle, PartCategory, Parts, PartFiles, PartImage, Distributor
from django.utils.timezone import now


admin.site.register(StorageLocation)
admin.site.register(Vehicle)
admin.site.register(PartCategory)


class BaseAdminInline(admin.StackedInline):
    extra = 0
    min_num = 0
    max_num = 1


class PartImageInline(BaseAdminInline):
    model = PartImage
    fields = ['image_tag', 'image', 'title']
    readonly_fields = ['image_tag', 'created_at']
    max_num = 20
    fk_name = 'part'


class PartFilesInline(BaseAdminInline):
    model = PartFiles
    fields = ['file', 'title']
    readonly_fields = ['created_at']
    max_num = 20
    fk_name = 'part'


class DistributorInline(BaseAdminInline):
    model = Distributor
    fields = ['distributor', 'weblink', 'part_number', 'price', 'quantity']
    readonly_fields = ['created_at']
    max_num = 20
    fk_name = 'part'


class PartAdminForm(forms.ModelForm):
    class Meta:
        model = Parts
        fields = ['part_number', 'name', 'manufacturer', 'category', 'quantity', 'storage_location', 'description']
        read_only_fields = ['cheapest_price', 'in_stock']

    def __init__(self, *args, **kwargs):
        super(PartAdminForm, self).__init__(*args, **kwargs)
        if Parts.objects.all().exists():
            query = Parts.objects.all().latest('id')
            self.fields['storage_location'].initial = query.storage_location
            self.fields['manufacturer'].initial = query.manufacturer
            self.fields['category'].initial = query.category
        self.fields['part_number'].initial = int(now().timestamp())


@admin.register(Parts)
class PartsAdmin(admin.ModelAdmin):
    model = Parts
    list_display = ('name', 'manufacturer', 'category', 'quantity', 'in_stock', 'cheapest_price')
    search_fields = ('name', 'manufacturer__name', 'category__name')
    list_filter = ('storage_location', 'manufacturer', 'category', 'in_stock')
    readonly_fields = ['cheapest_price', 'in_stock']
    form = PartAdminForm
    inlines = [PartImageInline, PartFilesInline, DistributorInline]
