from django.db import models

# Create your models here.
from django.utils import timezone
from django_tenants.models import TenantMixin, DomainMixin
from django.utils.translation import gettext_lazy as _

from apps.auth_user.models import User
from core.constants import AU_STATE_CHOICES
from core.django.validators import NumberOnlyValidator


class Domain(DomainMixin):
    pass


class Manager(User, TenantMixin):
    pool_shop = models.OneToOneField('pool_shop.PoolShop', blank=False, null=False, on_delete=models.CASCADE)


class Staff(User, TenantMixin):
    pool_shop = models.ForeignKey('pool_shop.PoolShop', blank=False, null=False, on_delete=models.CASCADE)


class PoolShop(models.Model):
    abn = models.CharField(_('abn'), max_length=11, blank=False, validators=[NumberOnlyValidator()])
    phone_number = models.CharField(_('phone number'), max_length=16, blank=False)

    address1 = models.CharField(_('address1'), max_length=250, blank=False)
    address2 = models.CharField(_('address1'), max_length=250, blank=True)
    suburb = models.CharField(_('suburb'), max_length=250, blank=False)
    city = models.CharField(_('city'), max_length=250, blank=False)
    post_code = models.CharField(_('post code'), max_length=4, blank=False, validators=[NumberOnlyValidator()])
    state = models.CharField(verbose_name="state", choices=AU_STATE_CHOICES, max_length=255, blank=True, null=False)

    is_active = models.BooleanField(_('active'), default=True, help_text='Active or in active.')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
