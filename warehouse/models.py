from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True


class Manufacturer(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    website = models.URLField(verbose_name=_("Website"), blank=True, null=True)

    class Meta:
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")
        constraints = [
            models.UniqueConstraint(fields=['name', 'website'], name='unique_manufacturer')
        ]

    def __str__(self):
        return self.name


class Warehouse(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        constraints = [
            models.UniqueConstraint(fields=['name', 'location'], name='unique_warehouse')
        ]

    def __str__(self):
        return f"{self.name} ({self.location})"


class AssortmentBox(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name=_("Warehouse"))

    class Meta:
        verbose_name = _("Assortment Box")
        verbose_name_plural = _("Assortment Boxes")
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
        constraints = [
            models.UniqueConstraint(fields=['number', 'assortment_box'], name='unique_compartment')
        ]

    def __str__(self):
        return f"{self.assortment_box} - {self.number}"
