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

