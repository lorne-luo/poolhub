from django.db import models

# Create your models here.
from django_tenants.models import TenantMixin
from apps.auth_user.models import User
from django.utils.translation import gettext_lazy as _

from core.constants import AU_STATE_CHOICES, CHLORINE_SOURCE_CHOICES, POOL_SURFACE_CHOICES, POOL_TYPE_CHOICES
from core.django.validators import NumberOnlyValidator


class Customer(User):
    address1 = models.CharField(_('address1'), max_length=250, blank=False)
    address2 = models.CharField(_('address1'), max_length=250, blank=True)
    suburb = models.CharField(_('suburb'), max_length=250, blank=False)
    city = models.CharField(_('city'), max_length=250, blank=False)
    post_code = models.CharField(_('post code'), max_length=4, blank=False, validators=[NumberOnlyValidator()])
    state = models.CharField(verbose_name="state", choices=AU_STATE_CHOICES, max_length=255, blank=True, null=False)


class Pool(models.Model):
    customer = models.ForeignKey('Customer', blank=False, null=False, on_delete=models.CASCADE)
    type = models.CharField(verbose_name="pool type", choices=POOL_TYPE_CHOICES, max_length=32, blank=True, null=False)
    chlorine_source = models.CharField(verbose_name="chlorine source", choices=CHLORINE_SOURCE_CHOICES, max_length=32,
                                       blank=True, null=False)
    pool_surface = models.CharField(verbose_name="pool surface", choices=POOL_SURFACE_CHOICES, max_length=32,
                                    blank=True, null=False)
    # pool data
    volume = models.IntegerField(_('volume litre'), blank=False)  # litre
