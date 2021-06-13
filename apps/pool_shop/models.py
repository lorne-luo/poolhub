from django.db import models, connection

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.auth_user.models import User
from core.constants import AU_STATE_CHOICES
from core.django.validators import NumberOnlyValidator


class PoolShopManager(models.Manager):
    def basic(self):
        return super(PoolShopManager, self).get_queryset().defer(
            'address1', 'address2', 'suburb', 'city', 'post_code', 'state')

    def address(self):
        return super(PoolShopManager, self).get_queryset().only(
            'address1', 'address2', 'suburb', 'city', 'post_code', 'state')


class PoolShop(models.Model):
    tenant = models.ForeignKey('tenant.Tenant', blank=False, null=False, on_delete=models.CASCADE)
    schema_name = models.CharField(max_length=63, blank=True)

    name = models.CharField(_('name'), max_length=255, blank=True)
    abn = models.CharField(_('abn'), max_length=11, blank=False, validators=[NumberOnlyValidator()])
    phone_number = models.CharField(_('phone number'), max_length=16, blank=True)
    email = models.CharField(_('email'), max_length=255, blank=True)

    address1 = models.CharField(_('address1'), max_length=250, blank=False)
    address2 = models.CharField(_('address2'), max_length=250, blank=True)
    suburb = models.CharField(_('suburb'), max_length=250, blank=False)
    city = models.CharField(_('city'), max_length=250, blank=False)
    post_code = models.CharField(_('post code'), max_length=4, blank=False, validators=[NumberOnlyValidator()])
    state = models.CharField(verbose_name="state", choices=AU_STATE_CHOICES, max_length=255, blank=True, null=False)

    is_active = models.BooleanField(_('active'), default=True, help_text='Active or in active.')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = PoolShopManager()

    def get_schema_name(self):
        if self.schema_name:
            return self.schema_name
        self.schema_name = self.tenant.schema_name
        self.save(update_fields=['schema_name'])
        return self.schema_name

    def set_schema(self):
        schema_name = self.get_schema_name()
        if schema_name:
            connection.set_schema(schema_name)


class PoolShopStaffMixin:
    pass


class Manager(PoolShopStaffMixin, User):
    pool_shop = models.OneToOneField('pool_shop.PoolShop', blank=False, null=False, on_delete=models.CASCADE)


class Staff(PoolShopStaffMixin, User):
    pool_shop = models.ForeignKey('pool_shop.PoolShop', blank=False, null=False, on_delete=models.CASCADE)
