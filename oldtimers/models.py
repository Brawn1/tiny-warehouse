from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from warehouse.models.warehouse import BaseModel, Warehouse, Manufacturer
from decimal import Decimal


class StorageLocation(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name=_("Warehouse"))

    class Meta:
        verbose_name = _("Storage Location")
        verbose_name_plural = _("Storage Locations")
        constraints = [
            models.UniqueConstraint(fields=['name', 'warehouse'], name='unique_storage_location')
        ]

    def __str__(self):
        return f"{self.name} - {self.warehouse}"


class Vehicle(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    vehicle_model = models.CharField(max_length=255, verbose_name=_("Model"))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_("Manufacturer"))
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True, verbose_name=_("Image"))
    datasheet = models.FileField(upload_to='datasheets/', blank=True, null=True, verbose_name=_("Datasheet"))
    model_year = models.PositiveIntegerField(verbose_name=_("Model Year"), default=timezone.now().year)
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    vehicle_number = models.CharField(max_length=255, verbose_name=_("Vehicle Number"), blank=True, null=True)
    engine_type = models.CharField(max_length=255, verbose_name=_("Engine"), blank=True, null=True)

    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")
        constraints = [
            models.UniqueConstraint(fields=['name', 'manufacturer'], name='unique_vehicle')
        ]

    def __str__(self):
        return f"{self.name} - {self.manufacturer}"


class PartCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Part Category")
        verbose_name_plural = _("Part Categories")

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')


class Parts(BaseModel):
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE, verbose_name=_("Storage Location"),
                                         blank=True, null=True)
    part_number = models.CharField(max_length=255, verbose_name=_("Part Number"), blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), default=0)
    in_stock = models.BooleanField(verbose_name=_("In Stock"), default=False)

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"), blank=True, default=0)
    # cheapest_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Cheapest Price"), blank=True,
    #                                      default=0)

    category = models.ForeignKey(PartCategory, on_delete=models.CASCADE, verbose_name=_("Category"), blank=True,
                                 null=True)

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_("Manufacturer"),
                                     blank=True, null=True)

    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        constraints = [
            models.UniqueConstraint(fields=['part_number', 'name', 'manufacturer'], name='unique_old_part_manufacturer'),
            models.UniqueConstraint(fields=['part_number', 'name'], name='unique_old_part')
        ]
        ordering = ['part_number', 'name']

    def __str__(self):
        return f"{self.name} - {self.manufacturer}"

    @property
    def cheapest_price(self) -> 'Decimal':
        if self.part_distributors.all().exists():
            return self.part_distributors.all().order_by('price').first().price
        return Decimal(0.0)

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.in_stock = True
        super(Parts, self).save(*args, **kwargs)


class PartImage(models.Model):
    image = models.ImageField(upload_to='parts/images/%Y/', verbose_name=_("Image"))
    title = models.CharField(max_length=255, verbose_name=_("Title"), blank=True, null=True)
    part = models.ForeignKey(Parts, on_delete=models.CASCADE, verbose_name=_("Part"), related_name='part_images')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"), editable=False)

    class Meta:
        verbose_name = _("Part Image")
        verbose_name_plural = _("Part Images")
        ordering = ['-created_at', 'part__name']

    def __str__(self):
        return f"{self.part} - {self.title}"

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')


class PartFiles(models.Model):
    file = models.FileField(upload_to='parts/datasheet/%Y/', verbose_name=_("Datasheet"))
    title = models.CharField(max_length=255, verbose_name=_("Title"), blank=True, null=True)
    part = models.ForeignKey(Parts, on_delete=models.CASCADE, verbose_name=_("Part"), related_name='part_files')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"), editable=False)

    class Meta:
        verbose_name = _("Part File")
        verbose_name_plural = _("Part Files")
        ordering = ['-created_at', 'part__name']

    def __str__(self):
        return f"{self.part} - {self.title}"


class Distributor(BaseModel):
    part = models.ForeignKey(Parts, on_delete=models.CASCADE, verbose_name=_("Part"), related_name='part_distributors')
    distributor = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_("Distributor"))
    weblink = models.URLField(verbose_name=_("Web Link"), blank=True, null=True)
    part_number = models.CharField(max_length=255, verbose_name=_("Part Number"), blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Sales Price"), blank=True,
                                default=0)
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), default=0)

    def __str__(self):
        return f"{self.distributor} - {self.part_number}"

