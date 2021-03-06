from django.db import models
from django.contrib.auth.models import Group
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField

# Create your models here.

OnlyNumbersValidator = RegexValidator(
    r'^[0-9]*$',
    'Only 0-9 are allowed.',
    'Invalid Number'
)

ServiceCodeValidator = RegexValidator(
    r'^[125679][024][01234567]$',
    'Please enter a valid Service Code',
    'Invalid Service Code'
)

class RateTable(models.Model):
    name = models.CharField(
        max_length=32,
    )
    tenant = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )
    effective_date = models.DateTimeField(
        verbose_name='Effective Date'
    )
    telco = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        verbose_name='Telco'
        )
    spare = models.CharField(
        max_length=32,
        validators=[
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Spare',
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'tenant'),)
        verbose_name = 'Rate Table'
        verbose_name_plural = 'Rate Tables'
