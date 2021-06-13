import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from core.aws.s3 import AWSS3URLs


class Testing(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=False, null=False)
    create_at = models.DateTimeField(_('date joined'), default=timezone.now)
    customer = models.ForeignKey('customer.Customer', blank=False, null=False, on_delete=models.CASCADE)
    photo = models.ImageField(blank=False, null=False, verbose_name='photo')  # upload_to='',
    s3_key = models.CharField(verbose_name="photo url", max_length=1024, blank=True, null=False)  # s3 key

    # reading
    # calcium hardness: 0-14
    ch = models.IntegerField(verbose_name="calcium hardness", blank=True, null=True,
                             validators=[MinValueValidator(0), MaxValueValidator(1000)])

    # free chlorine: 0-10
    fc = models.DecimalField(verbose_name="free chlorine", max_digits=4, decimal_places=2, blank=True, null=True,
                             validators=[MinValueValidator(0), MaxValueValidator(10)])

    # total chlorine: 0-10
    tc = models.DecimalField(verbose_name="total chlorine", max_digits=4, decimal_places=2, blank=True, null=True,
                             validators=[MinValueValidator(0), MaxValueValidator(10)])

    # total bromine: 0-20
    tb = models.DecimalField(verbose_name="total bromine", max_digits=4, decimal_places=2, blank=True, null=True,
                             validators=[MinValueValidator(0), MaxValueValidator(20)])

    # ph: 0-14
    ph = models.DecimalField(verbose_name="ph", max_digits=4, decimal_places=2, blank=True, null=True)

    # total alkainity: 0-240
    ta = models.IntegerField(verbose_name="total alkainity", blank=True, null=True,
                             validators=[MinValueValidator(0), MaxValueValidator(240)])

    # cyanuric acid: 0-300
    ca = models.IntegerField(verbose_name="cyanuric acid", blank=True, null=True,
                             validators=[MinValueValidator(0), MaxValueValidator(300)])

    @cached_property
    def photo_url(self):
        if self.photo:
            return AWSS3URLs.get_url(self.photo)
        return None


class TestResult(models.Model):
    customer = models.ForeignKey('customer.Customer', blank=False, null=False, on_delete=models.CASCADE)
    testing = models.ForeignKey('testing.Testing', blank=False, null=False, on_delete=models.CASCADE)
