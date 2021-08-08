import os
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, connection

from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from core.aws.s3 import AWSS3URLs


def tenant_strip_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    schema_name = connection.get_schema()
    return os.path.join('strip', schema_name)


class Testing(models.Model):
    """I"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=False, null=False)
    create_at = models.DateTimeField(_('date created'), default=timezone.now)
    customer = models.ForeignKey('customer.Customer', blank=True, null=True, on_delete=models.CASCADE)

    original_image = models.ImageField(blank=False, null=False, verbose_name='original image', upload_to=tenant_strip_path)
    crop_coordinate = models.JSONField( verbose_name='crop coordinate',blank=True, null=True)
    strip_crop = models.ImageField(blank=True, null=True, verbose_name='strip crop', upload_to=tenant_strip_path)

    s3_key = models.CharField(verbose_name="photo url", max_length=1024, blank=True, null=False)  # s3 key

    # prediction value
    # calcium hardness: 0-14
    th_value = models.IntegerField(verbose_name="calcium hardness", blank=True, null=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(1000)])
    # free chlorine: 0-10
    fc_value = models.DecimalField(verbose_name="free chlorine", max_digits=4, decimal_places=2, blank=True, null=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(10)])
    # total chlorine: 0-10
    tc_value = models.DecimalField(verbose_name="total chlorine", max_digits=4, decimal_places=2, blank=True, null=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(10)])
    # total bromine: 0-20
    tb_value = models.DecimalField(verbose_name="total bromine", max_digits=4, decimal_places=2, blank=True, null=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(20)])
    # ph: 0-14
    ph_value = models.DecimalField(verbose_name="ph", max_digits=4, decimal_places=2, blank=True, null=True)
    # total alkainity: 0-240
    ta_value = models.IntegerField(verbose_name="total alkainity", blank=True, null=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(240)])
    # cyanuric acid: 0-300
    ca_value = models.IntegerField(verbose_name="cyanuric acid", blank=True, null=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(300)])

    @cached_property
    def photo_url(self):
        if self.original_image:
            return AWSS3URLs.get_url(self.original_image)
        return None

    def set_crop_coordinate(self,arr):
        self.crop_coordinate=[int(i) for i in arr]
