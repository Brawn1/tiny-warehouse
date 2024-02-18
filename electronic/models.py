from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from warehouse.models.warehouse import BaseModel, Warehouse, Manufacturer


class AssortmentBox(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name=_("Warehouse"))

    class Meta:
        verbose_name = _("Assortment Box")
        verbose_name_plural = _("Assortment Boxes")
        ordering = ['name', 'warehouse__name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'warehouse'], name='unique_assortment_box')
        ]

    def __str__(self):
        return f"{self.name} - {self.warehouse}"


class PartCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name=_("Image"))

    class Meta:
        ordering = ['name']
        verbose_name = _("Part Category")
        verbose_name_plural = _("Part Categories")

    def __str__(self):
        return self.name


class Part(BaseModel):

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_("Manufacturer"))
    image = models.ImageField(upload_to='parts/', blank=True, null=True, verbose_name=_("Image"))
    datasheet = models.FileField(upload_to='datasheets/', blank=True, null=True, verbose_name=_("Datasheet"))
    category = models.ForeignKey(PartCategory, on_delete=models.CASCADE, verbose_name=_("Category"))
    part_type = models.CharField(max_length=255, verbose_name=_("Part Type"), blank=True, null=True)  # New field

    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        constraints = [
            models.UniqueConstraint(fields=['name', 'manufacturer'], name='unique_part')
        ]
        ordering = ['name', 'manufacturer__name']

    def __str__(self):
        return f"{self.name} - {self.manufacturer}"


class Compartment(BaseModel):
    number = models.PositiveIntegerField(verbose_name=_("Number"))
    part = models.ForeignKey(Part, on_delete=models.CASCADE, verbose_name=_("Part"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), default=0)
    assortment_box = models.ForeignKey(AssortmentBox, on_delete=models.CASCADE, verbose_name=_("Assortment Box"))

    class Meta:
        verbose_name = _("Compartment")
        verbose_name_plural = _("Compartments")
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['number', 'assortment_box', 'part'], name='unique_compartment')
        ]
        ordering = ['assortment_box', 'number']

    def __str__(self):
        return f"{self.assortment_box} - {self.number}"
