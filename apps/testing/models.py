import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from core.aws.s3 import AWSS3URLs


class Testing(models.Model):
    """I"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=False, null=False)
    create_at = models.DateTimeField(_('date created'), default=timezone.now)
    customer = models.ForeignKey('customer.Customer', blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(blank=False, null=False, verbose_name='image')  # upload_to='',
    s3_key = models.CharField(verbose_name="photo url", max_length=1024, blank=True, null=False)  # s3 key

    # accurate value
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
        if self.image:
            return AWSS3URLs.get_url(self.image)
        return None


class TrainTesting(models.Model):
    image = models.ImageField(blank=False, null=False, verbose_name='image')  # upload_to='',
    create_at = models.DateTimeField(_('date created'), default=timezone.now)

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

    # prediction
    ch_predict = models.IntegerField(verbose_name="calcium hardness", blank=True, null=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(1000)])
    fc_predict = models.DecimalField(verbose_name="free chlorine", max_digits=4, decimal_places=2, blank=True,
                                     null=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(10)])
    tc_predict = models.DecimalField(verbose_name="total chlorine", max_digits=4, decimal_places=2, blank=True,
                                     null=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(10)])
    tb_predict = models.DecimalField(verbose_name="total bromine", max_digits=4, decimal_places=2, blank=True,
                                     null=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(20)])
    ph_predict = models.DecimalField(verbose_name="ph", max_digits=4, decimal_places=2, blank=True, null=True)
    ta_predict = models.IntegerField(verbose_name="total alkainity", blank=True, null=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(240)])
    ca_predict = models.IntegerField(verbose_name="cyanuric acid", blank=True, null=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(300)])
