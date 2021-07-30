import os
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, connection

from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class TrainTesting(models.Model):
    original_image = models.ImageField(blank=False, null=False, verbose_name='original image',
                                       upload_to=os.path.join('strip', 'train'))
    crop_coordinate = models.JSONField( verbose_name='crop coordinate',blank=True, null=True)
    strip_crop = models.ImageField(blank=True, null=True, verbose_name='image',
                                   upload_to=os.path.join('strip', 'train'))

    create_at = models.DateTimeField(_('date created'), default=timezone.now)

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
